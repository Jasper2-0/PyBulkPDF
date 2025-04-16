# -*- coding: utf-8 -*-
"""
Command-Line Interface (CLI) setup and execution logic for PyBulkPDF.

Handles argument parsing and orchestrates calls to core functionality
based on the selected mode ('generate-template' or 'fill-form').
"""

import argparse
import logging
import sys
import os # Keep os import for path operations if needed here

# --- Relative Imports from within the package ---
from .core.template_generator import generate_template_files
from .core.form_filler import fill_pdf_forms # Import the actual function

# Import validation utility
from .utils.validation import prepare_output_directory
# Note: check_file_exists is imported within core modules where needed

# --- Logging Setup ---
from .utils.logging_setup import setup_logging
setup_logging() # Configure logging as soon as cli module is loaded

# --- Placeholder Functions ---
# Removed placeholder for generate_template_files
# Removed placeholder for fill_pdf_forms

# --- Main CLI Function ---
def main() -> None:
    """
    Parses command-line arguments, prepares the environment, and calls the
    appropriate function based on the selected mode.
    """
    parser = argparse.ArgumentParser(
        description="PyBulkPDF: Fill PDF forms from Excel (.xlsx) data.",
        formatter_class=argparse.RawTextHelpFormatter # Preserves formatting in help text
        )

    # Define subparsers for the two modes
    subparsers = parser.add_subparsers(
        dest='mode',
        required=True,
        help='Choose the operation mode: "generate-template" or "fill-form"'
        )

    # --- Subparser for Template Generation ---
    parser_gen = subparsers.add_parser(
        'generate-template',
        help='Analyze a PDF form and generate template files (XLSX Table and TXT).'
        )
    parser_gen.add_argument(
        '--template', '-t',
        required=True,
        help='Path to the input PDF form template file.'
        )
    parser_gen.add_argument(
        '--output-dir', '-o',
        required=True,
        help='Directory to save the generated template XLSX and field info TXT files.'
        )
    # Link to the *imported* function
    parser_gen.set_defaults(func=lambda args: generate_template_files(args.template, args.output_dir))

    # --- Subparser for Form Filling ---
    parser_fill = subparsers.add_parser(
        'fill-form',
        help='Fill PDF forms using data from an Excel (.xlsx) file.'
        )
    parser_fill.add_argument(
        '--template', '-t',
        required=True,
        help='Path to the input PDF form template file.'
        )
    parser_fill.add_argument(
        '--data-file', '-d',
        required=True,
        help='Path to the input Excel (.xlsx) data file (based on generated template).'
        )
    parser_fill.add_argument(
        '--output-dir', '-o',
        required=True,
        help='Directory to save the filled PDF output files.'
        )
    parser_fill.add_argument(
        '--overwrite',
        action='store_true', # Flag, doesn't take a value
        help='Allow overwriting existing files in the output directory. Use with caution.'
        )
    # Link to the *imported* function
    parser_fill.set_defaults(func=lambda args: fill_pdf_forms(args.template, args.data_file, args.output_dir, args.overwrite))

    # --- Parse Arguments ---
    args = parser.parse_args()

    # --- Prepare Output Directory and Execute Selected Mode ---
    output_dir_to_check = args.output_dir

    try:
        # Use the imported prepare_output_directory function
        if args.mode == 'generate-template':
            # Template generation allows outputting to an existing (non-empty) directory
            prepare_output_directory(output_dir_to_check, require_empty=False, allow_overwrite=True) # Allow overwrite implicitly for template gen
            # Call the function associated with the subparser
            args.func(args)

        elif args.mode == 'fill-form':
            # Form filling requires the directory to be empty unless --overwrite is specified
            prepare_output_directory(output_dir_to_check, require_empty=True, allow_overwrite=args.overwrite)
            # Call the function associated with the subparser
            args.func(args)

    except SystemExit as e:
         # Raised by sys.exit() in helper functions or here on fatal errors
         logging.critical("Execution halted due to fatal error.")
         sys.exit(e.code if e.code is not None else 1) # Exit with specific code if available
    except Exception as e:
         # Catch any other unexpected errors in the main execution flow
         logging.critical(f"An unexpected error occurred in CLI execution: {e}", exc_info=True)
         sys.exit(1)

# Note: No `if __name__ == "__main__":` block here,
# execution starts from pybulkpdf/__main__.py
