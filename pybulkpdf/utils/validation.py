# -*- coding: utf-8 -*-
"""
Utility functions for validating file paths and preparing directories.
Raises FileOperationError on failures.
"""

import os
import sys # Keep sys import for now, although exit calls are removed
import logging

# --- Relative Imports ---
from ..exceptions import FileOperationError # Import custom exception

# --- File and Directory Validation Functions ---

def check_file_exists(filepath: str) -> None:
    """
    Checks if a file exists at the given path and is actually a file.

    Args:
        filepath: The path to the file to check.

    Raises:
        FileOperationError: If the path does not exist or is not a file.
    """
    if not os.path.exists(filepath):
        msg = f"Input file not found: {filepath}"
        logging.error(msg)
        raise FileOperationError(msg) # Raise custom exception
    if not os.path.isfile(filepath):
        msg = f"Input path is not a file: {filepath}"
        logging.error(msg)
        raise FileOperationError(msg) # Raise custom exception
    # Log success at DEBUG level if needed
    logging.debug(f"File exists and is valid: {filepath}")

def prepare_output_directory(dirpath: str, require_empty: bool = False, allow_overwrite: bool = False) -> None:
    """
    Checks and prepares the output directory. Creates it if non-existent.
    Optionally checks if it's empty based on parameters.

    Args:
        dirpath: The path to the output directory.
        require_empty: If True, checks if the directory is empty (unless allow_overwrite is True).
                       Defaults to False.
        allow_overwrite: If True, suppresses the "not empty" error when require_empty is True.
                         Defaults to False.

    Raises:
        FileOperationError: If the path exists but is not a directory,
                            if directory creation fails, or if the directory
                            is required to be empty but is not (and overwrite is False).
    """
    if os.path.exists(dirpath):
        # Path exists, check if it's a directory
        if not os.path.isdir(dirpath):
            msg = f"Output path '{dirpath}' exists but is not a directory."
            logging.error(msg)
            raise FileOperationError(msg) # Raise custom exception

        # Path is a directory, check if it needs to be empty
        if require_empty and not allow_overwrite and os.listdir(dirpath):
            # Log error and raise exception
            msg = f"Output directory '{dirpath}' is not empty. Use --overwrite flag or specify a different directory."
            logging.error(msg)
            raise FileOperationError(msg) # Raise custom exception
            # Could define DirectoryNotEmptyError later if needed

        elif require_empty and allow_overwrite and os.listdir(dirpath):
            # Log warning if overwriting into a non-empty directory
            logging.warning(f"Output directory '{dirpath}' is not empty. Files may be overwritten.")
        # If directory exists, is valid, and passes emptiness check (if required), log usage.
        logging.info(f"Using existing output directory: {dirpath}")

    else:
        # Path does not exist, try to create it
        try:
            os.makedirs(dirpath)
            logging.info(f"Created output directory: {dirpath}")
        except (OSError, PermissionError) as e: # Catch potential errors during creation
            msg = f"Error creating output directory '{dirpath}'"
            logging.error(f"{msg}: {e}")
            # Wrap original exception for context
            raise FileOperationError(msg, original_exception=e) # Raise custom exception
