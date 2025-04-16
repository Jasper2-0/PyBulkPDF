# -*- coding: utf-8 -*-
"""
Custom exception classes for the PyBulkPDF application.

Provides a structured way to handle specific error conditions encountered
during PDF processing, Excel handling, configuration, and file operations.
"""

class PyBulkPDFError(Exception):
    """Base class for all custom exceptions in PyBulkPDF."""
    def __init__(self, message: str, original_exception: Exception | None = None):
        super().__init__(message)
        self.original_exception = original_exception

    def __str__(self) -> str:
        if self.original_exception:
            return f"{super().__str__()} (Original error: {self.original_exception})"
        return super().__str__()

# --- PDF Related Errors ---
class PDFProcessingError(PyBulkPDFError):
    """Base class for errors related to PDF processing."""
    pass

class PDFReadError(PDFProcessingError):
    """Error encountered while reading or parsing a PDF file."""
    pass

class PDFWriteError(PDFProcessingError):
    """Error encountered while writing or modifying a PDF file."""
    pass

# --- Excel Related Errors ---
class ExcelProcessingError(PyBulkPDFError):
    """Base class for errors related to Excel file processing."""
    pass

class ExcelReadError(ExcelProcessingError):
    """Error encountered while reading or parsing an Excel file."""
    pass

class ExcelWriteError(ExcelProcessingError):
    """Error encountered while writing an Excel file."""
    pass

# --- Configuration Errors ---
class ConfigurationError(PyBulkPDFError):
    """Error related to application configuration or input data structure."""
    pass

# --- File/Directory Operation Errors ---
class FileOperationError(PyBulkPDFError):
    """Error related to file or directory operations (permissions, existence etc.)."""
    pass

# Example of more specific file error (optional)
# class DirectoryNotEmptyError(FileOperationError):
#     """Raised when an output directory is not empty and overwrite is false."""
#     pass

