"""Script runner for QuickDeploy."""

import os
import subprocess
import sys
import signal
import threading
from pathlib import Path
from typing import Optional, Callable, Dict
from rich.console import Console
from rich.panel import Panel

from .config import QuickDeployConfig
from .env_manager import EnvManager
from .utils import detect_framework, find_entrypoint
from .watcher import FileWatcher


console = Console()


class ProcessRunner:
    """Manages running Python processes with logging and hot reload."""

    def __init__(self, project_path: Path, config: QuickDeployConfig):
        self.project_path = Path(project_path).resolve()
        self.config = config
        self.env_manager = EnvManager(self.project_path)
        self.process: Optional[subprocess.Popen] = None
        self.watcher: Optional[FileWatcher] = None
        self.log_callbacks: list[Callable[[str], None]] = []
        self.is_running = False
        self._stop_event = threading.Event()
    
    def add_log_callback(self, callback: Callable[[str], None]) -> None:
        """Add a callback for log output."""
        self.log_callbacks.append(callback)
    
    def _log(self, message: str, level: str = "info") -> None:
        """Emit log message to all callbacks."""
        for callback in self.log_callbacks:
            try:
                callback(message)
            except Exception:
                pass
    
    def _stream_output(self) -> None:
        """Stream process output to callbacks."""
        if not self.process:
            return
        
        try:
            for line in iter(self.process.stdout.readline, b''):
                if not line:
                    break
                
                try:
                    text = line.decode('utf-8', errors='replace').rstrip()
                    self._log(text)
                except Exception:
                    pass

                if self._stop_event.is_set():
                    break
        except Exception as e:
            self._log(f"Error reading output: {e}", "error")
    
    def _stream_error(self) -> None:
        """Stream process errors to callbacks."""
        if not self.process:
            return
        
        try:
            for line in iter(self.process.stderr.readline, b''):
                if not line:
                    break
                
                try:
                    text = line.decode('utf-8', errors='replace').rstrip()
                    self._log(text, "error")
                except Exception:
                    pass

                if self._stop_event.is_set():
                    break
        except Exception as e:
            self._log(f"Error reading stderr: {e}", "error")
    
    def _detect_and_format_url(self, line: str) -> Optional[str]:
        """Detect FastAPI/Flask URLs in log output and format them."""
        line_lower = line.lower()
        
        # FastAPI/Uvicorn patterns
        if "uvicorn running on" in line_lower or "application startup complete" in line_lower:
            url = f"http://127.0.0.1:{self.config.port}"
            return f"\n[bold green]→ Application running at: {url}[/bold green]\n"
        
        # Flask patterns
        if "running on" in line_lower and ("flask" in line_lower or "werkzeug" in line_lower):
            url = f"http://127.0.0.1:{self.config.port}"
            return f"\n[bold green]→ Application running at: {url}[/bold green]\n"

        # Generic port detection
        if f":{self.config.port}" in line or f"port {self.config.port}" in line_lower:
            url = f"http://127.0.0.1:{self.config.port}"
            return f"\n[bold green]→ Application running at: {url}[/bold green]\n"

        return None

    def run(self) -> bool:
        """Run the entrypoint script."""
        if self.is_running:
            self._log("Process is already running", "warning")
            return False

        # Ensure environment is set up
        if not self.env_manager.ensure_setup(
            python_version=self.config.python_version,
            install_deps=True
        ):
            self._log("Failed to set up environment", "error")
            return False

        # Find entrypoint
        entrypoint = find_entrypoint(self.project_path, self.config.entrypoint)
        if not entrypoint:
            self._log(f"Entrypoint not found: {self.config.entrypoint}", "error")
            return False

        # Detect framework and adjust command
        framework = detect_framework(entrypoint)
        python_exe = self.env_manager.get_python()

        # Build command
        if framework == "fastapi":
            # Try to run with uvicorn
            cmd = [
                str(python_exe), "-m", "uvicorn",
                entrypoint.stem + ":app",
                "--host", "127.0.0.1",
                "--port", str(self.config.port),
                "--reload" if self.config.auto_reload else ""
            ]
            cmd = [c for c in cmd if c]  # Remove empty strings
        elif framework == "flask":
            # Run Flask app
            env = {**os.environ, **self.config.env_vars}
            env["FLASK_APP"] = str(entrypoint)
            env["FLASK_ENV"] = "development"
            env["FLASK_RUN_PORT"] = str(self.config.port)
            cmd = [str(python_exe), str(entrypoint)]
        else:
            # Generic Python script
            cmd = [str(python_exe), str(entrypoint)]

        # Set environment variables
        env = {**os.environ, **self.config.env_vars}

        self._log(f"Starting: {' '.join(cmd)}")
        self._log(f"Working directory: {self.project_path}")

        try:
            # Start process
            self.process = subprocess.Popen(
                cmd,
                cwd=self.project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                bufsize=1
            )

            self.is_running = True
            self._stop_event.clear()

            # Start output streaming threads
            stdout_thread = threading.Thread(target=self._stream_output, daemon=True)
            stderr_thread = threading.Thread(target=self._stream_error, daemon=True)
            stdout_thread.start()
            stderr_thread.start()

            # Start file watcher if auto_reload is enabled
            if self.config.auto_reload:
                self.watcher = FileWatcher(
                    self.project_path,
                    self.restart,
                    self.config.watch_patterns,
                    self.config.ignore_patterns
                )
                self.watcher.start()
                self._log("Hot reload enabled - watching for file changes")

            return True

        except Exception as e:
            self._log(f"Failed to start process: {e}", "error")
            self.is_running = False
            return False

    def stop(self) -> None:
        """Stop the running process."""
        if not self.is_running:
            return

        self._stop_event.set()

        if self.watcher:
            self.watcher.stop()
            self.watcher = None

        if self.process:
            try:
                # Try graceful shutdown
                if sys.platform == "win32":
                    self.process.terminate()
                else:
                    self.process.send_signal(signal.SIGTERM)

                # Wait a bit
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill
                    self.process.kill()
                    self.process.wait()

            except Exception as e:
                self._log(f"Error stopping process: {e}", "error")
            finally:
                self.process = None

        self.is_running = False
        self._log("Process stopped")

    def restart(self) -> None:
        """Restart the process (for hot reload)."""
        self._log("\n[cyan]File change detected - restarting...[/cyan]\n")
        self.stop()
        # Small delay to ensure cleanup
        import time
        time.sleep(0.5)
        self.run()

    def wait(self) -> int:
        """Wait for process to complete and return exit code."""
        if self.process:
            return self.process.wait()
        return 0
