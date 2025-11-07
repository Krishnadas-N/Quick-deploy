"""Tkinter GUI application for QuickDeploy."""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from pathlib import Path
import threading
from typing import Optional

from ..core.config import load_config, create_default_config
from ..core.runner import ProcessRunner
from ..core.utils import find_entrypoint


class QuickDeployGUI:
    """Main GUI application for QuickDeploy."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QuickDeploy")
        self.root.geometry("900x700")
        
        self.project_path: Optional[Path] = None
        self.runner: Optional[ProcessRunner] = None
        self.config = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Project selection
        ttk.Label(main_frame, text="Project Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        self.path_var = tk.StringVar(value="No project selected")
        self.path_label = ttk.Label(path_frame, textvariable=self.path_var, anchor=tk.W)
        self.path_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(path_frame, text="Browse", command=self.browse_project).grid(row=0, column=1, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.run_button = ttk.Button(button_frame, text="Run", command=self.run_project, state=tk.DISABLED)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_project, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.config_button = ttk.Button(button_frame, text="Config", command=self.show_config, state=tk.DISABLED)
        self.config_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Status: Idle")
        self.status_label = ttk.Label(button_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Logs area
        ttk.Label(main_frame, text="Logs:").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.logs_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Consolas", 10)
        )
        self.logs_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Config info
        self.config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="5")
        self.config_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.config_info = ttk.Label(self.config_frame, text="No project loaded", anchor=tk.W)
        self.config_info.pack(fill=tk.X)
    
    def browse_project(self):
        """Browse for a project directory."""
        path = filedialog.askdirectory(title="Select Project Directory")
        if path:
            self.load_project(Path(path))
    
    def load_project(self, path: Path):
        """Load a project."""
        self.project_path = path.resolve()
        self.path_var.set(str(self.project_path))
        
        # Load config
        self.config = load_config(self.project_path)
        
        # Check for entrypoint
        entrypoint = find_entrypoint(self.project_path, self.config.entrypoint)
        if not entrypoint:
            messagebox.showwarning(
                "No Entrypoint",
                f"No entrypoint found. Please create {self.config.entrypoint} or edit .quickdeploy.yaml"
            )
            self.config_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.NORMAL)
            self.config_button.config(state=tk.NORMAL)
        
        # Update config info
        info_text = f"Entrypoint: {self.config.entrypoint} | Port: {self.config.port} | Reload: {'Yes' if self.config.auto_reload else 'No'}"
        self.config_info.config(text=info_text)
        
        self.log(f"Project loaded: {self.project_path}")
    
    def log(self, message: str):
        """Add a message to the logs."""
        self.logs_text.insert(tk.END, message + "\n")
        self.logs_text.see(tk.END)
        self.root.update_idletasks()
    
    def run_project(self):
        """Run the project."""
        if not self.project_path:
            return
        
        if self.runner and self.runner.is_running:
            messagebox.showinfo("Already Running", "Project is already running!")
            return
        
        self.log("=" * 60)
        self.log("Starting QuickDeploy...")
        self.log(f"Project: {self.project_path.name}")
        self.log(f"Entrypoint: {self.config.entrypoint}")
        self.log(f"Port: {self.config.port}")
        self.log("=" * 60)
        
        # Create runner
        self.runner = ProcessRunner(self.project_path, self.config)
        self.runner.add_log_callback(self.log)
        
        # Run in thread
        def run_thread():
            if self.runner.run():
                self.root.after(0, lambda: self.status_var.set("Status: Running"))
                self.root.after(0, lambda: self.run_button.config(state=tk.DISABLED))
                self.root.after(0, lambda: self.stop_button.config(state=tk.NORMAL))
            else:
                self.root.after(0, lambda: self.status_var.set("Status: Error"))
                self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
                messagebox.showerror("Error", "Failed to start project")
        
        threading.Thread(target=run_thread, daemon=True).start()
    
    def stop_project(self):
        """Stop the running project."""
        if self.runner and self.runner.is_running:
            self.log("Stopping project...")
            self.runner.stop()
            self.status_var.set("Status: Idle")
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log("Project stopped")
        else:
            messagebox.showinfo("Not Running", "No project is currently running")
    
    def show_config(self):
        """Show and edit configuration."""
        if not self.project_path:
            return
        
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration")
        config_window.geometry("600x500")
        
        # Config editor
        editor_frame = ttk.Frame(config_window, padding="10")
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(editor_frame, text=".quickdeploy.yaml:").pack(anchor=tk.W)
        
        config_text = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, font=("Consolas", 10))
        config_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load current config
        config_path = self.project_path / ".quickdeploy.yaml"
        if config_path.exists():
            config_text.insert("1.0", config_path.read_text(encoding="utf-8"))
        else:
            # Show default
            import yaml
            config_text.insert("1.0", yaml.dump(self.config.to_dict(), default_flow_style=False))
        
        # Buttons
        button_frame = ttk.Frame(config_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def save_config():
            try:
                content = config_text.get("1.0", tk.END)
                config_path.write_text(content, encoding="utf-8")
                # Reload
                self.config = load_config(self.project_path)
                messagebox.showinfo("Success", "Configuration saved!")
                config_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save config: {e}")
        
        ttk.Button(button_frame, text="Save", command=save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=config_window.destroy).pack(side=tk.RIGHT)


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = QuickDeployGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

