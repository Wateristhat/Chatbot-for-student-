"""
Logging utilities for the chatbot application.
Provides standard logging configuration with optional rich formatting.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Default configuration
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_DIR = Path("logs")


def setup_logging(
    level: str = None,
    log_file: Optional[str] = None,
    log_dir: Optional[Path] = None,
    enable_rich: bool = None,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None
) -> Dict[str, Any]:
    """
    Setup application logging with optional rich console formatting.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file name (if None, logs to console only)
        log_dir: Directory for log files (creates if doesn't exist)
        enable_rich: Whether to use rich console formatting (auto-detect if None)
        format_string: Custom log format string
        date_format: Custom date format string
        
    Returns:
        Dictionary with logging configuration info
    """
    # Get configuration from environment or use defaults
    log_level = (level or 
                os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)).upper()
    
    log_directory = log_dir or Path(os.getenv("LOG_DIR", str(DEFAULT_LOG_DIR)))
    
    # Auto-detect rich availability if not specified
    if enable_rich is None:
        enable_rich = os.getenv("ENABLE_RICH_LOGGING", "").lower() == "true"
        if enable_rich:
            try:
                import rich
                enable_rich = True
            except ImportError:
                enable_rich = False
    
    # Create log directory if needed
    if log_file:
        log_directory.mkdir(exist_ok=True, parents=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Setup console handler
    console_handler = _create_console_handler(
        enable_rich=enable_rich,
        format_string=format_string,
        date_format=date_format
    )
    root_logger.addHandler(console_handler)
    
    # Setup file handler if requested
    file_handler = None
    log_file_path = None
    if log_file:
        log_file_path = log_directory / log_file
        file_handler = _create_file_handler(
            log_file_path,
            format_string=format_string,
            date_format=date_format
        )
        if file_handler:
            root_logger.addHandler(file_handler)
    
    # Configure specific loggers for common libraries
    _configure_library_loggers()
    
    # Return configuration info
    config_info = {
        "level": log_level,
        "rich_enabled": enable_rich,
        "console_handler": console_handler is not None,
        "file_handler": file_handler is not None,
        "log_file": str(log_file_path) if log_file_path else None,
        "handlers_count": len(root_logger.handlers)
    }
    
    # Log initial message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized: level={log_level}, rich={enable_rich}, "
                f"file={'enabled' if log_file else 'disabled'}")
    
    return config_info


def _create_console_handler(
    enable_rich: bool = False,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None
) -> logging.Handler:
    """Create console handler with optional rich formatting."""
    
    if enable_rich:
        try:
            from rich.console import Console
            from rich.logging import RichHandler
            
            console = Console(stderr=True, force_terminal=True)
            handler = RichHandler(
                console=console,
                show_time=True,
                show_path=False,
                rich_tracebacks=True,
                tracebacks_show_locals=False
            )
            
            # Rich handler doesn't use standard formatters
            return handler
            
        except ImportError:
            # Fall back to standard handler if rich not available
            pass
    
    # Standard console handler
    handler = logging.StreamHandler(sys.stderr)
    
    # Set formatter
    formatter = logging.Formatter(
        fmt=format_string or DEFAULT_LOG_FORMAT,
        datefmt=date_format or DEFAULT_LOG_DATE_FORMAT
    )
    handler.setFormatter(formatter)
    
    return handler


def _create_file_handler(
    log_file_path: Path,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None
) -> Optional[logging.FileHandler]:
    """Create file handler for logging to file."""
    
    try:
        handler = logging.FileHandler(
            log_file_path,
            mode='a',
            encoding='utf-8'
        )
        
        # Set formatter
        formatter = logging.Formatter(
            fmt=format_string or DEFAULT_LOG_FORMAT,
            datefmt=date_format or DEFAULT_LOG_DATE_FORMAT
        )
        handler.setFormatter(formatter)
        
        return handler
        
    except Exception as e:
        print(f"Failed to create file handler for {log_file_path}: {e}", file=sys.stderr)
        return None


def _configure_library_loggers():
    """Configure logging levels for common third-party libraries."""
    
    # Reduce noise from common libraries
    library_levels = {
        'urllib3': logging.WARNING,
        'requests': logging.WARNING,
        'openai': logging.WARNING,
        'google': logging.WARNING,
        'streamlit': logging.WARNING,
        'PIL': logging.WARNING,
        'matplotlib': logging.WARNING,
        'httpx': logging.WARNING,
        'httpcore': logging.WARNING,
    }
    
    for lib_name, level in library_levels.items():
        logging.getLogger(lib_name).setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name (typically __name__ of the module)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_function_call(func_name: str, args: Dict[str, Any] = None, level: str = "DEBUG"):
    """
    Log a function call with its arguments.
    
    Args:
        func_name: Name of the function being called
        args: Dictionary of function arguments
        level: Log level for the message
    """
    logger = logging.getLogger("function_calls")
    log_level = getattr(logging, level.upper(), logging.DEBUG)
    
    if args:
        args_str = ", ".join([f"{k}={v}" for k, v in args.items()])
        message = f"Calling {func_name}({args_str})"
    else:
        message = f"Calling {func_name}()"
    
    logger.log(log_level, message)


def log_performance(operation: str, duration: float, details: Dict[str, Any] = None):
    """
    Log performance metrics for operations.
    
    Args:
        operation: Name of the operation
        duration: Duration in seconds
        details: Additional performance details
    """
    logger = logging.getLogger("performance")
    
    details_str = ""
    if details:
        details_items = [f"{k}={v}" for k, v in details.items()]
        details_str = f" ({', '.join(details_items)})"
    
    logger.info(f"Performance: {operation} took {duration:.3f}s{details_str}")


def create_session_logger(session_id: str) -> logging.Logger:
    """
    Create a logger for a specific session/user.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Session-specific logger
    """
    logger_name = f"session.{session_id}"
    logger = logging.getLogger(logger_name)
    
    # Add session context to messages
    if not logger.handlers:
        # Create a custom formatter that includes session ID
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f"%(asctime)s | {session_id} | %(levelname)s | %(message)s",
            datefmt=DEFAULT_LOG_DATE_FORMAT
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Don't duplicate in root logger
    
    return logger


class ContextLogger:
    """Context manager for logging with additional context."""
    
    def __init__(self, logger: logging.Logger, operation: str, **context):
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        context_str = ", ".join([f"{k}={v}" for k, v in self.context.items()])
        self.logger.debug(f"Starting {self.operation} ({context_str})")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.debug(f"Completed {self.operation} in {duration:.3f}s")
        else:
            self.logger.error(f"Failed {self.operation} after {duration:.3f}s: {exc_val}")
        
        return False  # Don't suppress exceptions


# Quick setup functions
def setup_basic_logging(level: str = "INFO") -> Dict[str, Any]:
    """Quick setup for basic console logging."""
    return setup_logging(level=level, enable_rich=False)


def setup_rich_logging(level: str = "INFO") -> Dict[str, Any]:
    """Quick setup for rich console logging."""
    return setup_logging(level=level, enable_rich=True)


def setup_file_logging(
    log_file: str = "app.log",
    level: str = "INFO",
    enable_rich_console: bool = True
) -> Dict[str, Any]:
    """Quick setup for file + console logging."""
    return setup_logging(
        level=level,
        log_file=log_file,
        enable_rich=enable_rich_console
    )


# Initialize default logging if this module is imported
if __name__ != "__main__":
    # Only setup logging if not running as script
    # This allows the module to be imported without side effects
    pass