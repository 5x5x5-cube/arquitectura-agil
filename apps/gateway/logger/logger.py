import csv
import datetime
import os
from typing import Optional, Dict, Any

class Logger:
    def __init__(self, log_file: str = "app.log"):
        self.log_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_path = os.path.join(self.log_dir, log_file)
        self._ensure_log_file()

    def _ensure_log_file(self):
        """Create log file and headers if it doesn't exist"""
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['timestamp', 'type', 'message', 'details'])

    def log(self, message: str, log_type: str = 'info', details: Optional[Dict[str, Any]] = None):
        """
        Log a message with specified type and optional details
        
        Args:
            message: The log message
            log_type: Type of log (info, warning, error)
            details: Optional dictionary with additional details
        """
        timestamp = datetime.datetime.now().isoformat()
        with open(self.log_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                log_type.lower(),
                message,
                str(details) if details else ''
            ])

    def info(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.log(message, 'info', details)

    def warning(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.log(message, 'warning', details)

    def error(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.log(message, 'error', details)
