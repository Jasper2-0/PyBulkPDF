# Project Description: PyBulkPDF Mail Merge CLI

## 1. Introduction & Purpose

This project aims to create a command-line interface (CLI) tool written in Python to automate the process of filling PDF forms using data from an Excel spreadsheet (`.xlsx`). Specifically, it addresses the need to perform mail-merge operations on PDF grading forms, providing a cross-platform alternative to other solutions.

The tool leverages the `pypdf` library to interact with PDF documents and `openpyxl` for handling Excel files.

## 2. Core Features

* **Command-Line Interface:** Interaction via standard CLI arguments using `argparse`.
* **PDF Form Analysis:** Analyzes an input PDF form template to identify fillable fields.
* **Template Generation:** Creates:
  * An Excel (`.xlsx`) template file with headers corresponding to the PDF form fields, plus a dedicated `_output_filename` header. The sheet is automatically formatted as an Excel Table for better usability.
  * A companion text file (`_field_info.txt`) detailing expected values for non-text fields (checkboxes, radio buttons, dropdowns).
* **Excel-Driven Form Filling:** Reads data from a user-populated Excel file and fills a copy of the PDF template for each data row.
* **Dynamic Filename Generation:** Uses filenames specified by the user within the `_output_filename` column of the input Excel sheet for saving each filled PDF.
* **Configurable Output:** Saves generated PDF files to a user-specified output directory.
* **Robust Error Handling:** Includes checks for file existence, directory status, data mismatches, and PDF/Excel processing errors.
* **User Feedback:** Provides informative, colored console logging and a progress bar during form filling.
* **Overwrite Option:** Allows users to optionally overwrite files in the output directory.

## 3. Workflow

The tool operates in two distinct modes:

**Mode 1: Template Generation (`generate-template`)**

1. **Input:** Path to the PDF form template (`--template`), output directory for templates (`--output-dir`).
2. **Process:**
    * The script reads the PDF template using `pypdf`.
    * It identifies all fillable form fields and their types.
    * It generates a `[TemplateName]_template.xlsx` file in the specified output directory. This Excel file contains headers for all PDF fields plus an `_output_filename` header, formatted as an Excel Table.
    * It generates a `[TemplateName]_field_info.txt` file in the same directory, listing non-text fields and attempting to identify their expected input values (e.g., `/Yes`, `/Off`, specific choice options).
3. **Output:** `_template.xlsx` and `_field_info.txt` files.

**Mode 2: Form Filling (`fill-form`)**

1. **Input:** Path to the PDF form template (`--template`), path to the filled Excel data file (`--data-file`), path to the desired output directory (`--output-dir`), and an optional `--overwrite` flag.
2. **Pre-Checks:**
    * Verify all input files exist.
    * Check the output directory:
        * If it doesn't exist, create it.
        * If it exists and is empty, proceed.
        * If it exists and is *not* empty, require the `--overwrite` flag to proceed (with a warning).
    * Verify the Excel sheet contains the `_output_filename` column.
3. **Processing:**
    * Read the PDF template fields.
    * Read the Excel data row by row (skipping empty rows).
    * Compare Excel headers and PDF fields, logging warnings for mismatches.
    * For each data row:
        * Read the target filename from the `_output_filename` column.
        * Create a mapping of PDF field names to the corresponding data in the current Excel row (converting values to strings).
        * Use `pypdf` to fill a *clone* of the template with this data, attempting updates on all pages.
        * Save the filled PDF to the output directory using the specified filename.
        * Log success or failure for the row.
    * Provide a summary of successes and failures at the end.
4. **Output:** Multiple filled PDF files in the specified output directory.

## 4. Technical Details

* **Language:** Python 3.7+
* **Core Libraries:**
  * `pypdf` (for PDF manipulation)
  * `openpyxl` (for reading/writing `.xlsx` files)
* **Key Modules:**
  * `argparse` (for CLI argument parsing)
  * `logging` (for user feedback and error reporting)
  * `os`, `sys` (for file/directory operations and system interaction)
  * `colorama` (for colored console output)
  * `tqdm` (for progress bars)
* **Platform:** Cross-platform (developed with macOS compatibility in mind, tested on standard OS).

## 5. Error Handling Strategy

* **Fatal Errors:** Invalid arguments, missing input files, inability to create/access output directory, missing critical `_output_filename` Excel column, inability to read template fields or Excel headers.
* **Non-Fatal Warnings/Skips:** Mismatched Excel columns/PDF fields (fields won't be filled/ignored), empty `_output_filename` for a row, errors during `pypdf` processing or file saving for a specific row (logs error, skips row/file, continues), non-empty output directory without `--overwrite`.
* **User Intervention:** None required during runtime after initial checks pass (unless a critical error occurs).

## 6. Future Considerations (Optional)

* Development of a simple GUI (e.g., using Tkinter, PyQt, CustomTkinter).
* Support for other spreadsheet formats (e.g., `.ods`, potentially `.csv` as an option).
* More sophisticated field type detection and value validation.
