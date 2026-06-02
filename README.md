# 📄 docx-to-csv-json

A Python utility that parses structured academic `.docx` files (specifically **Ruminant Science** journal archives) and exports the extracted data to **CSV** or **JSON** format — ready for WordPress import or data pipelines.

---

## What It Does

Given a `.docx` file containing journal article listings, the script extracts:

| Field | Description |
|---|---|
| `archive_date` | Parsed from header line (e.g. `June-2024-13-1`) |
| `title` | Article title with index number |
| `title_2` | Formatted title block with Authors & Source (HTML-ready for JSON) |
| `content` | Full abstract/body content per article |

---

## Project Structure

```
python_csv_script/
│
├── src/
│   ├── docx_to_csv.py        # Extracts to CSV (plain text output)
│   └── docx_to_json.py       # Extracts to JSON (HTML-formatted output)
│
├── docx_files/
│   ├── sample_input.docx     # Sample input file
│   └── 2024_ruminant_science_june.docx
│
├── output/
│   ├── output_file.csv
│   ├── output_file.json
│   └── output_file_sample.json
│
├── requirements.txt
├── test.py
└── README.md
```

---

## Input Format

The `.docx` file must follow this structure:

```
Ruminant Science June 2024(13-1)

Title: Effect of dietary supplementation on milk yield...
Authors: Singh A, Kumar B, Sharma C
Source: Ruminant Science, 13(1): 1-8

[Abstract text here...]

Title: Comparative study of breed performance...
Authors: Patel D, Gupta E
Source: Ruminant Science, 13(1): 9-15

[Abstract text here...]
```

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/docx-to-csv-json.git
cd docx-to-csv-json

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

## Usage

### Export to CSV

```bash
cd src
python docx_to_csv.py
```

Edit paths inside the script:
```python
input_file  = '../docx_files/sample_input.docx'
output_file = '../output/output_file.csv'
```

### Export to JSON

```bash
cd src
python docx_to_json.py
```

Edit paths inside the script:
```python
input_file  = '../docx_files/2024_ruminant_science_june.docx'
output_file = '../output/output_file.json'
```

---

## Output Examples

### CSV (`output_file.csv`)

```
archive_date,title,title_2,content
June-2024-13-1,1-Title: Effect of dietary...,1-Title: Effect of dietary...,"1-Title: ...
Authors: ...
Source: ...

Abstract text..."
```

### JSON (`output_file.json`)

```json
[
    {
        "archive_date": "June-2024-13-1",
        "title": "1-Title: Effect of dietary supplementation...",
        "title_2": "<b>1-Title:</b> Effect of dietary...\n<b>Authors:</b> Singh A...\n<b>Source:</b> ...",
        "content": "<b>1-Title:</b> ...\n\n<center><b>Abstract</b></center>\n\nAbstract text here..."
    }
]
```

The JSON output includes HTML tags (`<b>`, `<center>`) making it suitable for direct WordPress post import via a plugin like **JSON Post Mapper**.

---

## Difference Between CSV and JSON Scripts

| Feature | `docx_to_csv.py` | `docx_to_json.py` |
|---|---|---|
| Output format | `.csv` | `.json` |
| `title_2` formatting | Plain text | HTML (`<b>` tags) |
| Abstract section | Plain text | `<center><b>Abstract</b></center>` header added |
| Best for | Spreadsheet use | WordPress / CMS import |

---

## Requirements

```
python-docx
```

Install via:
```bash
pip install -r requirements.txt
```

Python 3.8+ recommended.

---

## License

MIT — free to use and modify.