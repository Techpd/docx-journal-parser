import re
import csv
from docx import Document

# Function to extract text from the .docx file
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():  # Only add non-empty lines
            full_text.append(para.text.strip())
    return full_text

# Function to parse the extracted text and create rows of data
def parse_document(text):
    rows = []

    # Regex patterns
    archive_date_pattern = re.compile(r'Ruminant Science\s+(\w+)\s+(\d{4})\((\d+)-(\d+)\)')
    title_pattern = re.compile(r'Title:\s*(.+)')
    authors_pattern = re.compile(r'Authors:\s*(.+)')
    source_pattern = re.compile(r'Source:\s*(.+)')

    current_row = {
        'archive_date': '',
        'title': '',
        'title_2': '',
        'content': ''
    }

    content_buffer = ''
    title_index = 1

    for line in text:
        archive_date_match = archive_date_pattern.search(line)
        title_match = title_pattern.search(line)
        authors_match = authors_pattern.search(line)
        source_match = source_pattern.search(line)

        if archive_date_match:
            month, year, volume, issue = archive_date_match.groups()
            current_row['archive_date'] = f"{month}-{year}-{volume}-{issue}"
            continue  # Skip this line from being added to the content

        if title_match:
            if current_row['title']:
                # Save the previous title's data with combined content
                current_row['content'] = current_row['title_2'] + "\n\n" + content_buffer.strip()
                rows.append(current_row)
                # Reset for new data
                content_buffer = ''
                title_index += 1

            # Capture title
            current_row = {
                'archive_date': current_row['archive_date'],
                'title': f"{title_index}-Title: {title_match.group(1)}",
                'title_2': f"{title_index}-Title: {title_match.group(1)}",
                'content': ''
            }
            title_2_parts = [current_row['title_2']]
            continue

        if authors_match:
            title_2_parts.append(f"Authors: {authors_match.group(1)}")

        if source_match:
            title_2_parts.append(f"Source: {source_match.group(1)}")

        if title_match or authors_match or source_match:
            # Join title_2 parts
            current_row['title_2'] = "\n".join(title_2_parts).strip()
        else:
            # Capture content until the next title
            content_buffer += line + "\n"

    # Save the last row
    if current_row['title']:
        current_row['content'] = current_row['title_2'] + content_buffer.strip()
        rows.append(current_row)

    return rows

# Function to export parsed data to a CSV file
def export_to_csv(data, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['archive_date', 'title', 'title_2', 'content']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main function
def docx_to_csv(input_file, output_file):
    # Step 1: Extract text from the docx file
    text = extract_text_from_docx(input_file)

    # Step 2: Parse the document to extract the required information
    parsed_data = parse_document(text)

    # Step 3: Export the parsed data to a CSV file
    export_to_csv(parsed_data, output_file)

# Example usage
input_file = '../docx_files/sample_input.docx'  # Path to the input .docx file
output_file = '../output/output_file.csv'  # Path to save the CSV file
docx_to_csv(input_file, output_file)

print("CSV extraction complete!")
