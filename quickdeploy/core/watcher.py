"""File watching and hot reload for QuickDeploy."""

import time
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class ReloadHandler(FileSystemEventHandler):
    """Handler for file system events that trigger reloads."""
    
    def __init__(self, callback: Callable[[], None], 
                 watch_patterns: list[str],
                 ignore_patterns: list[str]):
        self.callback = callback
        self.watch_patterns = watch_patterns
        self.ignore_patterns = ignore_patterns
        self.last_trigger = 0
        self.debounce_seconds = 0.5
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        path_str = str(path)
        
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if pattern in path_str or path.name.startswith("."):
                return True
        
        return False
    
    def should_watch(self, path: Path) -> bool:
        """Check if path matches watch patterns."""
        for pattern in self.watch_patterns:
            if path.match(pattern) or pattern.replace("*", "") in path.name:
                return True
        return False
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        
        if self.should_ignore(path):
            return
        
        if not self.should_watch(path):
            return
        
        # Debounce rapid changes
        current_time = time.time()
        if current_time - self.last_trigger < self.debounce_seconds:
            return
        
        self.last_trigger = current_time
        self.callback()
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        self.on_modified(event)


class FileWatcher:
    """Watches files for changes and triggers callbacks."""
    
    def __init__(self, project_path: Path,
                 callback: Callable[[], None],
                 watch_patterns: list[str],
                 ignore_patterns: list[str]):
        self.project_path = Path(project_path).resolve()
        self.callback = callback
        self.watch_patterns = watch_patterns
        self.ignore_patterns = ignore_patterns
        self.observer: Optional[Observer] = None
        self.handler: Optional[ReloadHandler] = None
    
    def start(self) -> None:
        """Start watching for file changes."""
        if self.observer is not None:
            return
        
        self.handler = ReloadHandler(
            self.callback,
            self.watch_patterns,
            self.ignore_patterns
        )
        
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.project_path), recursive=True)
        self.observer.start()
    
    def stop(self) -> None:
        """Stop watching for file changes."""
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.handler = None
    
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self.observer is not None and self.observer.is_alive()

