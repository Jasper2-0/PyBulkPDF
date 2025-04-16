# -*- coding: utf-8 -*-
"""
Unit tests for the pybulkpdf.utils.validation module using pytest.
"""

import pytest
import os # Still needed for some mock assertions

# --- Module to test ---
from pybulkpdf.utils import validation
from pybulkpdf.exceptions import FileOperationError

# Note: pytest automatically discovers and runs functions starting with 'test_'
# The 'mocker' fixture is provided by the pytest-mock plugin (usually installed with pytest)

# --- Tests for check_file_exists ---

def test_check_file_exists_success(mocker):
    """Test check_file_exists when file exists and is a file."""
    # Mock os.path functions using mocker fixture
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isfile = mocker.patch('os.path.isfile', return_value=True)

    # Call the function - should not raise an error
    validation.check_file_exists("path/to/existing/file.txt")

    # Assert mocks were called as expected
    mock_exists.assert_called_once_with("path/to/existing/file.txt")
    mock_isfile.assert_called_once_with("path/to/existing/file.txt")

def test_check_file_exists_not_found(mocker):
    """Test check_file_exists when file does not exist."""
    mock_exists = mocker.patch('os.path.exists', return_value=False)
    mock_isfile = mocker.patch('os.path.isfile') # Mock isfile as well

    # Use pytest.raises to assert that the correct exception is raised
    with pytest.raises(FileOperationError, match="Input file not found"):
        validation.check_file_exists("path/to/nonexistent/file.txt")

    mock_exists.assert_called_once_with("path/to/nonexistent/file.txt")
    mock_isfile.assert_not_called() # isfile shouldn't be called if exists is false

def test_check_file_exists_is_dir(mocker):
    """Test check_file_exists when path exists but is not a file."""
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isfile = mocker.patch('os.path.isfile', return_value=False) # Simulate path being a directory

    with pytest.raises(FileOperationError, match="Input path is not a file"):
        validation.check_file_exists("path/to/a/directory")

    mock_exists.assert_called_once_with("path/to/a/directory")
    mock_isfile.assert_called_once_with("path/to/a/directory")

# --- Tests for prepare_output_directory ---

def test_prepare_output_dir_does_not_exist(mocker):
    """Test prepare_output_directory creates dir if it doesn't exist."""
    mock_exists = mocker.patch('os.path.exists', return_value=False)
    mock_isdir = mocker.patch('os.path.isdir') # Mock isdir as well
    mock_makedirs = mocker.patch('os.makedirs')

    validation.prepare_output_directory("new/output/dir")

    mock_exists.assert_called_once_with("new/output/dir")
    mock_isdir.assert_not_called()
    mock_makedirs.assert_called_once_with("new/output/dir")

def test_prepare_output_dir_exists_is_dir(mocker):
    """Test prepare_output_directory uses existing directory."""
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isdir = mocker.patch('os.path.isdir', return_value=True)
    mock_makedirs = mocker.patch('os.makedirs')
    # Mock listdir as it might be called even if require_empty is False
    mocker.patch('os.listdir', return_value=[])

    # Assume require_empty=False (default)
    validation.prepare_output_directory("existing/output/dir")

    mock_exists.assert_called_once_with("existing/output/dir")
    mock_isdir.assert_called_once_with("existing/output/dir")
    mock_makedirs.assert_not_called()

def test_prepare_output_dir_exists_is_file(mocker):
    """Test prepare_output_directory raises error if path is a file."""
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isdir = mocker.patch('os.path.isdir', return_value=False) # Simulate path being a file
    mock_makedirs = mocker.patch('os.makedirs')

    with pytest.raises(FileOperationError, match="exists but is not a directory"):
        validation.prepare_output_directory("path/is/a/file.txt")

    mock_exists.assert_called_once_with("path/is/a/file.txt")
    mock_isdir.assert_called_once_with("path/is/a/file.txt")
    mock_makedirs.assert_not_called()

def test_prepare_output_dir_exists_not_empty_require_empty_no_overwrite(mocker):
    """Test prepare_output_directory raises error if dir not empty, require_empty=True, overwrite=False."""
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isdir = mocker.patch('os.path.isdir', return_value=True)
    mock_listdir = mocker.patch('os.listdir', return_value=['some_file.txt']) # Simulate non-empty
    mock_makedirs = mocker.patch('os.makedirs')

    with pytest.raises(FileOperationError, match="is not empty"):
        validation.prepare_output_directory("non_empty/dir", require_empty=True, allow_overwrite=False)

    mock_listdir.assert_called_once_with("non_empty/dir")
    mock_makedirs.assert_not_called() # Should not try to create dir

def test_prepare_output_dir_exists_not_empty_require_empty_with_overwrite(mocker):
    """Test prepare_output_directory succeeds if dir not empty, require_empty=True, overwrite=True."""
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isdir = mocker.patch('os.path.isdir', return_value=True)
    mock_listdir = mocker.patch('os.listdir', return_value=['some_file.txt'])
    mock_makedirs = mocker.patch('os.makedirs')
    # Mock logging to check for warning (optional, requires caplog fixture)
    # caplog fixture captures log messages

    # Should log a warning but not raise an error
    validation.prepare_output_directory("non_empty/dir", require_empty=True, allow_overwrite=True)
    # assert "directory is not empty. Files may be overwritten" in caplog.text # Example using caplog

    mock_listdir.assert_called_once_with("non_empty/dir")
    mock_makedirs.assert_not_called()

def test_prepare_output_dir_exists_empty_require_empty(mocker):
    """Test prepare_output_directory succeeds if dir empty and require_empty=True."""
    mock_exists = mocker.patch('os.path.exists', return_value=True)
    mock_isdir = mocker.patch('os.path.isdir', return_value=True)
    mock_listdir = mocker.patch('os.listdir', return_value=[]) # Simulate empty directory
    mock_makedirs = mocker.patch('os.makedirs')

    validation.prepare_output_directory("empty/dir", require_empty=True, allow_overwrite=False)

    mock_listdir.assert_called_once_with("empty/dir")
    mock_makedirs.assert_not_called()

def test_prepare_output_dir_creation_fails(mocker):
    """Test prepare_output_directory raises error if os.makedirs fails."""
    mock_exists = mocker.patch('os.path.exists', return_value=False)
    mock_isdir = mocker.patch('os.path.isdir')
    mock_makedirs = mocker.patch('os.makedirs', side_effect=OSError("Permission denied")) # Simulate failure

    with pytest.raises(FileOperationError, match="Error creating output directory"):
        validation.prepare_output_directory("uncreatable/dir")

    mock_makedirs.assert_called_once_with("uncreatable/dir")

# No need for if __name__ == '__main__': pytest handles discovery
