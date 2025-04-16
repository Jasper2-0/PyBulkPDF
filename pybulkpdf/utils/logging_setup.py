# -*- coding: utf-8 -*-
"""
Logging configuration for the PyBulkPDF tool.

Provides colored console output for different log levels.
"""

import logging
import colorama
from colorama import Fore, Style, init
from typing import Dict

# Initialize colorama for cross-platform colored output
# autoreset=True ensures style resets after each print
init(autoreset=True)

# --- Custom Colored Logging Formatter ---
class ColoredFormatter(logging.Formatter):
    """Custom logging formatter to add colors based on log level."""

    # Define colors for different log levels
    LEVEL_COLORS: Dict[int, str] = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with appropriate colors."""
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE) # Default to white if level unknown
        # Define the log format string with color codes
        # Example format: "INFO: Log message here" (colored)
        log_fmt = f"{color}{Style.BRIGHT}%(levelname)s{Style.RESET_ALL}: %(message)s"
        # Create a standard formatter with this format string
        formatter = logging.Formatter(log_fmt)
        # Format the record using the standard formatter
        return formatter.format(record)

# --- Logging Setup Function ---
def setup_logging(level: int = logging.INFO) -> None:
    """
    Configures the root logger for console output with colors.

    Args:
        level: The minimum logging level to display (e.g., logging.INFO, logging.DEBUG).
               Defaults to logging.INFO.
    """
    logger = logging.getLogger() # Get the root logger
    logger.setLevel(level)

    # Clear existing handlers to prevent duplicate messages if setup is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a console handler
    console_handler = logging.StreamHandler()
    # Set the custom colored formatter
    console_handler.setFormatter(ColoredFormatter())

    # Add the handler to the root logger
    logger.addHandler(console_handler)

    # Optional: Log a message indicating logging is configured
    # logging.debug("Colored logging configured.") # Use debug level for config messages
