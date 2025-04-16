# -*- coding: utf-8 -*-
"""
Unit tests for the pybulkpdf.core.pdf_analyzer.PDFAnalyzer class using pytest.
"""

import pytest
from unittest.mock import MagicMock # Can use MagicMock directly for complex mocks

# --- Module/Classes to test ---
# Use absolute imports from the package name
from pybulkpdf.core.pdf_analyzer import PDFAnalyzer
from pybulkpdf.exceptions import PDFReadError
from pybulkpdf import config

# --- Third-party library components to mock ---
from pypdf import errors as pypdf_errors

# --- Mock Data ---
MOCK_PDF_PATH = "dummy/path/doc.pdf"

MOCK_FIELDS_DATA = {
    "FieldName1": {"/T": "FieldName1", "/FT": "/Tx", "/V": "Value1"}, # Text field
    "CheckBoxField": {"/T": "CheckBoxField", "/FT": "/Btn", "/AP": {"/N": {"/Yes": "...", "/Off": "..."}}}, # Checkbox
    "ChoiceField": {"/T": "ChoiceField", "/FT": "/Ch", "/Opt": [("Display1", "Export1"), ("Display2", "Export2")]}, # Choice field
    "RadioButton": {"/T": "RadioButton", "/FT": "/Btn", "/AP": {"/N": {"/OptionA": "...", "/Off": "..."}}}, # Radio button (similar structure to checkbox)
}

MOCK_FIELDS_DATA_NO_NON_TEXT = {
    "Text1": {"/T": "Text1", "/FT": "/Tx", "/V": "Hello"},
    "Text2": {"/T": "Text2", "/FT": "/Tx", "/V": "World"},
}

# --- Test Suite ---

def test_pdf_analyzer_init_success_with_fields(mocker):
    """Test PDFAnalyzer initialization with a PDF containing fields."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = MOCK_FIELDS_DATA
    # Patch using absolute path
    mock_pdf_reader = mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)

    analyzer = PDFAnalyzer(MOCK_PDF_PATH)

    mock_pdf_reader.assert_called_once_with(MOCK_PDF_PATH)
    mock_reader_instance.get_fields.assert_called_once()
    assert analyzer.pdf_path == MOCK_PDF_PATH
    assert analyzer.fields == MOCK_FIELDS_DATA
    assert analyzer.field_names == set(MOCK_FIELDS_DATA.keys())

def test_pdf_analyzer_init_success_no_fields(mocker):
    """Test PDFAnalyzer initialization with a PDF containing no fields."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = None
    mock_pdf_reader = mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)

    analyzer = PDFAnalyzer(MOCK_PDF_PATH)

    mock_pdf_reader.assert_called_once_with(MOCK_PDF_PATH)
    mock_reader_instance.get_fields.assert_called_once()
    assert analyzer.fields is None
    assert analyzer.field_names == set()

def test_pdf_analyzer_init_pdf_read_error(mocker):
    """Test PDFAnalyzer initialization raises PDFReadError on pypdf error."""
    mock_pdf_reader = mocker.patch(
        'pybulkpdf.core.pdf_analyzer.PdfReader',
        side_effect=pypdf_errors.PdfReadError("Mock pypdf read error")
    )

    with pytest.raises(PDFReadError, match="Error reading PDF structure"):
        PDFAnalyzer(MOCK_PDF_PATH)

    mock_pdf_reader.assert_called_once_with(MOCK_PDF_PATH)

def test_pdf_analyzer_init_other_exception(mocker):
    """Test PDFAnalyzer initialization raises PDFReadError on unexpected error."""
    mock_pdf_reader = mocker.patch(
        'pybulkpdf.core.pdf_analyzer.PdfReader',
        side_effect=Exception("Mock unexpected error")
    )

    with pytest.raises(PDFReadError, match="Unexpected error opening or reading PDF"):
        PDFAnalyzer(MOCK_PDF_PATH)

    mock_pdf_reader.assert_called_once_with(MOCK_PDF_PATH)

# --- Tests for Getter Methods ---

def test_get_fields(mocker):
    """Test get_fields method returns correct data."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = MOCK_FIELDS_DATA
    mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
    analyzer = PDFAnalyzer(MOCK_PDF_PATH)
    assert analyzer.get_fields() == MOCK_FIELDS_DATA

def test_get_fields_no_fields(mocker):
    """Test get_fields method returns None when no fields."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = None
    mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
    analyzer = PDFAnalyzer(MOCK_PDF_PATH)
    assert analyzer.get_fields() is None

def test_get_field_names(mocker):
    """Test get_field_names method returns correct data."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = MOCK_FIELDS_DATA
    mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
    analyzer = PDFAnalyzer(MOCK_PDF_PATH)
    assert analyzer.get_field_names() == set(MOCK_FIELDS_DATA.keys())

def test_get_field_names_no_fields(mocker):
    """Test get_field_names method returns empty set when no fields."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = None
    mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
    analyzer = PDFAnalyzer(MOCK_PDF_PATH)
    assert analyzer.get_field_names() == set()

# --- Tests for analyze_field_types ---

@pytest.fixture # Use a fixture to create a pre-configured analyzer instance
def analyzer_with_mock_fields(mocker):
    """Fixture to provide a PDFAnalyzer instance with mocked fields."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = MOCK_FIELDS_DATA
    mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
    # Need to instantiate using the correct class path if patching constructor
    # This fixture implicitly uses the patched constructor
    return PDFAnalyzer(MOCK_PDF_PATH)


@pytest.fixture
def analyzer_with_no_fields(mocker):
    """Fixture to provide a PDFAnalyzer instance with no fields."""
    mock_reader_instance = MagicMock()
    mock_reader_instance.get_fields.return_value = None
    mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
    return PDFAnalyzer(MOCK_PDF_PATH)

@pytest.fixture
def analyzer_with_text_only(mocker):
     """Fixture for PDFAnalyzer with only text fields."""
     mock_reader_instance = MagicMock()
     mock_reader_instance.get_fields.return_value = MOCK_FIELDS_DATA_NO_NON_TEXT
     mocker.patch('pybulkpdf.core.pdf_analyzer.PdfReader', return_value=mock_reader_instance)
     return PDFAnalyzer(MOCK_PDF_PATH)


def test_analyze_field_types_mixed(analyzer_with_mock_fields):
    """Test analyze_field_types with mixed field types."""
    analysis = analyzer_with_mock_fields.analyze_field_types()
    assert len(analysis) == 3
    # Use list comprehension for cleaner checks regardless of order
    assert any("Field 'CheckBoxField' (Button): Expected values (e.g., /Yes)" in s for s in analysis)
    assert any("Field 'ChoiceField' (Choice): Expected values : Export1, Export2" in s for s in analysis)
    assert any("Field 'RadioButton' (Button): Expected values (e.g., /OptionA)" in s for s in analysis)


def test_analyze_field_types_text_only(analyzer_with_text_only):
    """Test analyze_field_types with only text fields."""
    analysis = analyzer_with_text_only.analyze_field_types()
    assert analysis == []

def test_analyze_field_types_no_fields(analyzer_with_no_fields):
    """Test analyze_field_types when PDF has no fields."""
    analysis = analyzer_with_no_fields.analyze_field_types()
    assert analysis == []

def test_analyze_field_types_load_failed(mocker):
    """Test analyze_field_types when PDF loading failed (fields=None)."""
    analyzer = PDFAnalyzer.__new__(PDFAnalyzer) # Create instance without calling __init__
    analyzer.fields = None # Manually set state after simulated load failure
    analysis = analyzer.analyze_field_types()
    assert analysis == []
