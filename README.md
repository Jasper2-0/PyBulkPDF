# PyBulkPDF: PDF Form Mail Merge CLI

PyBulkPDF is a Python command-line tool designed to automate the process of filling PDF form fields using data from an Excel spreadsheet (`.xlsx`). It acts as a mail merge utility specifically for PDF forms, providing a convenient way to generate multiple filled PDFs from a single template and data source.

## Features

* **Template Generation:** Analyzes a PDF form template to identify fillable fields and generates:
  * An Excel (`.xlsx`) template file with headers matching the PDF fields plus a required `_output_filename` column. The sheet is formatted as an Excel Table for ease of use.
  * A companion text file (`_field_info.txt`) detailing expected values for non-text fields (like checkboxes, radio buttons, dropdowns).
* **Excel-Driven Form Filling:** Reads data from a populated Excel file and fills a copy of the PDF template for each row.
* **Dynamic Output Filenames:** Uses the values in the `_output_filename` column of the Excel sheet to name each generated PDF.
* **User Feedback:** Provides informative console logging with colors for different message levels (INFO, WARNING, ERROR).
* **Progress Bar:** Displays a progress bar during the form-filling process.
* **Overwrite Option:** Includes an `--overwrite` flag for the `fill-form` mode to allow outputting to a non-empty directory.
* **Error Summary:** Summarizes any rows that failed during the filling process.

## Requirements

* Python 3.7+
* Dependencies (installable via `pip`):
  * `pypdf`
  * `openpyxl`
  * `colorama`
  * `tqdm`

## Installation

1. **Clone the repository (or download the script):**

    ```bash
    # Example if using Git:
    # git clone <your-repository-url>
    # cd PyBulkPDF
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate.bat` or `.venv\Scripts\Activate.ps1`
    ```

3. **Install dependencies:**
    (Ensure you have a `requirements.txt` file in the project root - see content provided separately)

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script operates in two main modes: `generate-template` and `fill-form`.

### 1. Generate Template Files**

This mode analyzes your PDF form and creates the necessary Excel template and field info file.

```bash
python pybulkpdf.py generate-template \
    --template /path/to/your/form_template.pdf \
    --output-dir /path/to/save/templates
```

* `--template` (`-t`): Path to the input PDF form template. (Required)
* `--output-dir` (`-o`): Directory where the generated `_template.xlsx` and `_field_info.txt` files will be saved. (Required)

### 2. Fill PDF Forms**

This mode reads your populated Excel file and generates the filled PDFs.

```bash
python pybulkpdf.py fill-form \
    --template /path/to/your/form_template.pdf \
    --data-file /path/to/your/filled_data.xlsx \
    --output-dir /path/to/save/filled_pdfs \
    [--overwrite]
```

* `--template` (`-t`): Path to the input PDF form template. (Required)
* `--data-file` (`-d`): Path to the input Excel data file (populated based on the generated template). (Required)
* `--output-dir` (`-o`): Directory where the filled PDF output files will be saved. This directory must be empty unless `--overwrite` is used. (Required)
* `--overwrite`: Optional flag to allow writing filled PDFs into a non-empty output directory. Existing files with the same name will be overwritten.

## Workflow

1. **Run `generate-template` mode:** Provide your blank PDF form to generate the `_template.xlsx` and `_field_info.txt` files.
2. **Populate the Excel Template:** Open the generated `_template.xlsx` file. Fill in the data for each PDF you want to create, one row per PDF.
    * Make sure to fill the `_output_filename` column with the desired filename for each corresponding output PDF (e.g., `student1_assessment.pdf`). The `.pdf` extension is optional; it will be added if missing.
    * Refer to the `_field_info.txt` file for guidance on values needed for checkboxes or dropdowns (e.g., `/Yes`, `/Off`, specific option text).
    * You can delete columns from the Excel sheet if you don't need to fill those specific PDF fields for this batch.
3. **Run `fill-form` mode:** Provide the original PDF template, your populated Excel data file, and an empty output directory. Add the `--overwrite` flag if you need to output into a directory that already contains files.
4. **Check Output:** The filled PDF files will be generated in the specified output directory. Review the console logs for a summary and any errors.

## License

(Consider adding a license here, e.g., MIT License)

```txt
MIT License

Copyright (c) 2025 [Jasper Schelling / Rotterdam University of Applied Sciences]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
