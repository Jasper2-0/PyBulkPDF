# -*- coding: utf-8 -*-
"""
Central configuration settings and constants for PyBulkPDF.
"""

import logging

# --- File Naming Conventions ---
OUTPUT_FILENAME_COL: str = "_output_filename"  # Mandatory column name in Excel for output PDF filenames
DEFAULT_SHEET_NAME: str = "Data"              # Default sheet name for generated Excel template
DEFAULT_TABLE_NAME: str = "PDFData"           # Default table name for formatted Excel table
FIELD_INFO_SUFFIX: str = "_field_info.txt"     # Suffix for the generated field info text file
TEMPLATE_SUFFIX: str = "_template.xlsx"      # Suffix for the generated Excel template file

# --- PDF Field Types (as defined in PDF specification) ---
# Used for identifying field types during analysis
FIELD_TYPE_BUTTON: str = '/Btn'  # Checkbox / Radio Button
FIELD_TYPE_CHOICE: str = '/Ch'   # Dropdown / Listbox
FIELD_TYPE_TEXT: str = '/Tx'    # Text Field
# Add other field types like '/Sig' (Signature) if needed later

# --- PDF Field Values (Common Examples) ---
# Common values used for checkboxes/radio buttons (may vary by PDF)
PDF_VALUE_CHECKBOX_ON: str = '/Yes'
PDF_VALUE_CHECKBOX_OFF: str = '/Off' # Often the default state when unchecked

# --- Logging Configuration ---
# Default logging level (can be overridden if CLI args are added for verbosity)
LOG_LEVEL: int = logging.INFO

# Color mapping for console logging (used by utils.logging_setup)
# Requires colorama to be installed
LOG_LEVEL_COLORS: dict[int, str] = {
    logging.DEBUG: "CYAN",      # Using string names for easier config if loaded from file later
    logging.INFO: "GREEN",
    logging.WARNING: "YELLOW",
    logging.ERROR: "RED",
    logging.CRITICAL: "MAGENTA_BRIGHT", # Custom name, handled in formatter
}
# Note: The actual Fore/Style objects are handled in the formatter itself.
# This dictionary provides the mapping. Consider refactoring formatter to use these names.

# --- Excel Settings ---
EXCEL_TABLE_STYLE: str = "TableStyleMedium9" # Default style for the generated Excel table

