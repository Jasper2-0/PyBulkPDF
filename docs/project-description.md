# Project Description: PyPDF Mail Merge CLI

## 1. Introduction & Purpose

This project aims to create a command-line interface (CLI) tool written in Python to automate the process of filling PDF forms using data from a CSV file. Specifically, it addresses the need to perform mail-merge operations on PDF grading forms on macOS, providing an alternative to Windows-only solutions like `BulkPDF` for this specific task.

The tool will leverage the `pypdf` library to interact with PDF documents.

## 2. Core Features

* **Command-Line Interface:** Interaction via standard CLI arguments.
* **PDF Form Analysis:** Analyzes an input PDF form template to identify fillable fields.
* **Template Generation:** Creates a CSV template file with headers corresponding to the PDF form fields, plus a dedicated `_output_filename` header. It also generates a companion `.txt` file detailing expected values for non-text fields (checkboxes, radio buttons).
* **CSV-Driven Form Filling:** Reads data from a user-populated CSV file and fills a copy of the PDF template for each data row.
* **Dynamic Filename Generation:** Uses filenames specified by the user within the `_output_filename` column of the input CSV for saving each filled PDF.
* **Data-Driven Date Insertion:** Populates date fields within the PDF using date information provided in the CSV data.
* **Configurable Output:** Saves generated PDF files to a user-specified output directory.
* **Robust Error Handling:** Includes checks for file existence, directory conflicts, data mismatches, and PDF processing errors.
* **User Feedback:** Provides informative console logging during operation.

## 3. Workflow

The tool operates in two distinct modes:

**Mode 1: Template Generation**

1.  **Input:** Path to the PDF form template (`--template`), output directory for templates (`--output-dir`), and a flag (`--generate-template`).
2.  **Process:**
    * The script reads the PDF template using `pypdf`.
    * It identifies all fillable form fields and their types.
    * It generates a `[TemplateName]_template.csv` file in the specified output directory. This CSV contains headers for all PDF fields plus an `_output_filename` header.
    * It generates a `[TemplateName]_field_info.txt` file in the same directory, listing non-text fields (checkboxes, radio buttons) and their expected input values (e.g., `/Yes`, `/Off`).
3.  **Output:** `_template.csv` and `_field_info.txt` files.

**Mode 2: Form Filling**

1.  **Input:** Path to the PDF form template (`--template`), path to the filled CSV data file (`--csv`), and path to the desired output directory (`--output-dir`).
2.  **Pre-Checks:**
    * Verify all input files exist.
    * Check the output directory:
        * If it doesn't exist, create it.
        * If it exists and is empty, proceed.
        * If it exists and is *not* empty, prompt the user to specify a different directory or cancel.
    * Verify the CSV contains the `_output_filename` column.
3.  **Processing:**
    * Read the PDF template fields.
    * Read the CSV data row by row.
    * Compare CSV headers and PDF fields, logging warnings for mismatches.
    * For each CSV row:
        * Read the target filename from the `_output_filename` column.
        * Create a mapping of PDF field names to the corresponding data in the current CSV row.
        * Use `pypdf` to fill a copy of the template with this data.
        * Save the filled PDF to the output directory using the specified filename.
        * Log success or failure for the row.
4.  **Output:** Multiple filled PDF files in the specified output directory.

## 4. Technical Details

* **Language:** Python 3.x
* **Core Library:** `pypdf` (for PDF manipulation)
* **Key Modules:**
    * `argparse` (for CLI argument parsing)
    * `csv` (for reading CSV data)
    * `logging` (for user feedback and error reporting)
    * `os` (for file/directory operations)
* **Platform:** Cross-platform (developed with macOS compatibility in mind).

## 5. Error Handling Strategy

* **Fatal Errors:** Invalid arguments, missing input files, inability to create output directory, missing critical `_output_filename` CSV column.
* **User Intervention:** Non-empty output directory prompts user for alternative or cancellation.
* **Non-Fatal Warnings/Skips:** Mismatched CSV columns/PDF fields, empty `_output_filename` for a row, errors during `pypdf` processing or file saving for a specific row (logs error, skips row/file, continues).

## 6. Future Considerations (Optional)

* Development of a simple GUI (e.g., using Tkinter, PyQt).
* Wrapping the core logic in a Web API (e.g., using Flask/FastAPI).
