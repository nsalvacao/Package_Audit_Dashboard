"""Structured logging configuration for Package Audit Dashboard."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in JSON format for production
    or human-readable format for development.
    """

    def __init__(self, json_format: bool = False, use_colors: bool = True):
        """
        Initialize the formatter.

        Args:
            json_format: If True, output logs in JSON format
            use_colors: If True, use ANSI colors in non-JSON format
        """
        super().__init__()
        self.json_format = json_format
        self.use_colors = use_colors and sys.stdout.isatty()

        # Level colors
        self.level_colors = {
            "DEBUG": CYAN,
            "INFO": GREEN,
            "WARNING": YELLOW,
            "ERROR": RED,
            "CRITICAL": f"{BOLD}{RED}",
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record."""
        if self.json_format:
            return self._format_json(record)
        return self._format_human(record)

    def _format_json(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        return json.dumps(log_data)

    def _format_human(self, record: logging.LogRecord) -> str:
        """Format log record in human-readable format with colors."""
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname
        name = record.name
        message = record.getMessage()

        # Apply colors
        if self.use_colors:
            level_color = self.level_colors.get(level, "")
            level_str = f"{level_color}{level:8}{RESET}"
            name_str = f"{MAGENTA}{name}{RESET}"
            timestamp_str = f"{BLUE}{timestamp}{RESET}"
        else:
            level_str = f"{level:8}"
            name_str = name
            timestamp_str = timestamp

        # Build log line
        log_line = f"{timestamp_str} | {level_str} | {name_str:30} | {message}"

        # Add exception if present
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            log_line += f"\n{exc_text}"

        return log_line


class StructuredLogger:
    """
    Enhanced logger with structured logging capabilities.
    """

    def __init__(self, name: str):
        """
        Initialize the structured logger.

        Args:
            name: Logger name (typically __name__)
        """
        self.logger = logging.getLogger(name)
        self._extra_context: dict[str, Any] = {}

    def with_context(self, **kwargs: Any) -> StructuredLogger:
        """
        Create a new logger instance with additional context.

        Args:
            **kwargs: Key-value pairs to add to log context

        Returns:
            New logger instance with added context
        """
        new_logger = StructuredLogger(self.logger.name)
        new_logger._extra_context = {**self._extra_context, **kwargs}
        return new_logger

    def _log(self, level: int, message: str, **kwargs: Any) -> None:
        """
        Internal logging method that adds context.

        Args:
            level: Log level
            message: Log message
            **kwargs: Additional context
        """
        extra_data = {**self._extra_context, **kwargs}
        self.logger.log(level, message, extra={"extra_data": extra_data})

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with context."""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with context."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with context."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with context."""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message with context."""
        self._log(logging.CRITICAL, message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback."""
        self.logger.exception(message, extra={"extra_data": {**self._extra_context, **kwargs}})


def setup_logging(
    log_level: str = "INFO",
    json_format: bool = False,
    log_file: str | None = None,
    use_colors: bool = True,
) -> None:
    """
    Configure application-wide logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON format for logs
        log_file: Optional file path for log output
        use_colors: Use colors in console output (ignored if json_format=True)
    """
    # Convert log level string to constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatter
    formatter = StructuredFormatter(json_format=json_format, use_colors=use_colors)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        # Always use JSON format for file logs
        file_formatter = StructuredFormatter(json_format=True, use_colors=False)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(numeric_level)
        root_logger.addHandler(file_handler)

    # Set levels for noisy libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name)


# Convenience function for request logging
def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: str | None = None,
) -> None:
    """
    Log HTTP request with structured data.

    Args:
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration_ms: Request duration in milliseconds
        user_id: Optional user identifier
    """
    logger = get_logger("http")
    logger.info(
        f"{method} {path} {status_code}",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=round(duration_ms, 2),
        user_id=user_id,
    )


# Convenience function for operation logging
def log_operation(
    operation: str,
    manager_id: str,
    package_name: str | None = None,
    success: bool = True,
    duration_ms: float | None = None,
    **kwargs: Any,
) -> None:
    """
    Log package manager operation with structured data.

    Args:
        operation: Operation name (uninstall, list, scan, etc.)
        manager_id: Package manager identifier
        package_name: Optional package name
        success: Whether operation succeeded
        duration_ms: Operation duration in milliseconds
        **kwargs: Additional context
    """
    logger = get_logger("operations")
    level_method = logger.info if success else logger.error

    message = f"{operation} on {manager_id}"
    if package_name:
        message += f": {package_name}"

    level_method(
        message,
        operation=operation,
        manager_id=manager_id,
        package_name=package_name,
        success=success,
        duration_ms=round(duration_ms, 2) if duration_ms else None,
        **kwargs,
    )
