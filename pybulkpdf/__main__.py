# -*- coding: utf-8 -*-
"""
Main entry point for the PyBulkPDF package when executed as a module.

Example:
    python -m pybulkpdf --help
"""

import sys
from .cli import main as cli_main # Relative import from cli.py

def main():
    """
    Executes the main command-line interface function.
    Handles potential exceptions during CLI execution.
    """
    try:
        cli_main()
    except Exception as e:
        # Basic fallback logging if logging setup itself failed or error is early
        print(f"An unexpected critical error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    except SystemExit as e:
        # Catch SystemExit to allow specific exit codes from cli_main
        sys.exit(e.code)


if __name__ == "__main__":
    main()
