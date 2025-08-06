"""
Logging configuration and utilities.
"""

import logging
import logging.config
import os
from pathlib import Path
from typing import Optional

import yaml
from pythonjsonlogger import jsonlogger


def setup_logging(
    config_path: Optional[str] = None,
    log_level: Optional[str] = None,
    log_format: Optional[str] = None
) -> None:
    """
    Set up logging configuration.
    
    Args:
        config_path: Path to logging configuration file
        log_level: Override log level
        log_format: Override log format
    """
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Override log level if specified
        if log_level:
            config['root']['level'] = log_level.upper()
            for logger_config in config['loggers'].values():
                logger_config['level'] = log_level.upper()
        
        # Override formatter if specified
        if log_format:
            if log_format.lower() == 'json':
                config['root']['handlers'] = ['console', 'file', 'error_file']
            else:
                config['root']['handlers'] = ['console', 'file', 'error_file']
        
        logging.config.dictConfig(config)
    else:
        # Default logging configuration
        setup_default_logging(log_level, log_format)


def setup_default_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None
) -> None:
    """
    Set up default logging configuration.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format (json, simple, detailed)
    """
    level = getattr(logging, (log_level or "INFO").upper())
    
    # Create formatters
    if log_format and log_format.lower() == "json":
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Create file handler
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


def log_function_call(func):
    """Decorator to log function calls."""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise
    return wrapper


def log_execution_time(func):
    """Decorator to log function execution time."""
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {e}")
            raise
    return wrapper 