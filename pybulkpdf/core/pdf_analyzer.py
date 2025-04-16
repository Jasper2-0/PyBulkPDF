# -*- coding: utf-8 -*-
"""
Analyzes PDF files to extract form fields and their properties.
"""

import logging
from typing import Dict, Any, Optional, List, Set

from pypdf import PdfReader
from pypdf import errors as pypdf_errors

# --- Relative Imports ---
from .. import config # Import the central config module
from ..exceptions import PDFReadError # Import custom PDF exception

class PDFAnalyzer:
    """
    Analyzes PDF files for form fields and their properties.

    Attributes:
        pdf_path (str): The path to the PDF file.
        fields (Optional[Dict[str, Any]]): Dictionary of extracted form fields. None if loading failed or no fields.
        field_names (Optional[Set[str]]): Set of field names. None if loading failed or no fields.

    Raises:
        PDFReadError: If the PDF file cannot be read or parsed during initialization.
    """

    def __init__(self, pdf_path: str):
        """
        Initializes the PDFAnalyzer and loads field data.

        Args:
            pdf_path (str): The path to the PDF file to analyze.

        Raises:
            PDFReadError: If loading the PDF fails.
        """
        self.pdf_path: str = pdf_path
        self.fields: Optional[Dict[str, Any]] = None
        self.field_names: Optional[Set[str]] = None
        self._load() # Load fields upon initialization, may raise PDFReadError

    def _load(self) -> None:
        """
        Loads the PDF and extracts fields.

        Raises:
            PDFReadError: If the PDF cannot be read or parsed.
        """
        try:
            # Assuming check_file_exists was called by the caller before instantiation
            reader = PdfReader(self.pdf_path)
            self.fields = reader.get_fields() # Can return None or dict
            if self.fields:
                self.field_names = set(self.fields.keys())
                logging.debug(f"Successfully loaded {len(self.field_names)} fields from {self.pdf_path}")
            else:
                # PDF has no fields, this is not an error state for the reader itself
                logging.warning(f"No fillable form fields found in '{self.pdf_path}'.")
                self.fields = None # Explicitly None if no fields
                self.field_names = set() # Empty set if no fields

        except pypdf_errors.PdfReadError as e:
            msg = f"Error reading PDF structure from '{self.pdf_path}'"
            logging.error(f"{msg}: {e}")
            # Raise custom exception, wrapping original
            raise PDFReadError(msg, original_exception=e)
        except FileNotFoundError as e: # Should be caught earlier, but as fallback
             msg = f"PDF file not found at '{self.pdf_path}'"
             logging.error(msg)
             raise PDFReadError(msg, original_exception=e) # Treat as PDF read issue in this context
        except Exception as e:
            # Catch other potential pypdf or general exceptions during loading
            msg = f"Unexpected error opening or reading PDF '{self.pdf_path}'"
            logging.error(f"{msg}: {e}")
            raise PDFReadError(msg, original_exception=e)

    def get_fields(self) -> Optional[Dict[str, Any]]:
        """Returns the dictionary of extracted fields."""
        # Returns None if _load failed or PDF had no fields
        return self.fields

    def get_field_names(self) -> Optional[Set[str]]:
        """Returns the set of extracted field names."""
        # Returns None if _load failed, empty set if PDF had no fields
        return self.field_names

    def analyze_field_types(self) -> List[str]:
        """
        Analyzes field properties to extract information about non-text fields.

        Returns:
            A list of strings describing non-text fields. Returns empty list
            if fields could not be loaded or no non-text fields found.
        """
        # If _load failed, self.fields will be None
        if not self.fields:
            return []

        non_text_fields_info: List[str] = []
        for name, properties in self.fields.items():
            field_type = properties.get('/FT')
            export_values: List[str] = []
            info: str = ""

            if field_type == config.FIELD_TYPE_BUTTON:
                ap_dict = properties.get('/AP', {})
                if hasattr(ap_dict, 'get'):
                    ap_n_dict = ap_dict.get('/N', {})
                    if isinstance(ap_n_dict, dict):
                        export_values = list(ap_n_dict.keys())
                if config.PDF_VALUE_CHECKBOX_OFF in export_values:
                    export_values.remove(config.PDF_VALUE_CHECKBOX_OFF)
                info = f"Field '{name}' (Button): Expected values "
                info += f"(e.g., {', '.join(export_values)})" if export_values else f"(Check PDF for values like {config.PDF_VALUE_CHECKBOX_ON}, /On)"
                non_text_fields_info.append(info)

            elif field_type == config.FIELD_TYPE_CHOICE:
                options = properties.get('/Opt', [])
                info = f"Field '{name}' (Choice): Expected values "
                if options:
                    if isinstance(options[0], (list, tuple)) and len(options[0]) >= 1:
                        export_values = [str(opt[1]) if len(opt) > 1 else str(opt[0]) for opt in options]
                    else:
                        export_values = [str(opt) for opt in options]
                info += f": {', '.join(export_values)}" if export_values else "(Check PDF for options)"
                non_text_fields_info.append(info)

        return non_text_fields_info
