import re
import csv
from docx import Document

# Function to extract text from the .docx file
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text.strip())
    return full_text

# Function to parse the extracted text and create rows of data
def parse_document(text):
    rows = []
    
    # Regex patterns
    archive_date_pattern = re.compile(r'Ruminant Science\s+(\w+)\s+(\d{4})\((\d+)-(\d+)\)')
    title_1_pattern = re.compile(r'(\d+)-Title:\s*(.+)')
    authors_pattern = re.compile(r'Authors:\s*(.+)')
    source_pattern = re.compile(r'Source:\s*(.+)')
    
    current_row = {
        'archive_date': '',
        'title': '',
        'title_2': '',
        'content': ''
    }
    
    content_buffer = ''
    found_title_1 = False

    for i, line in enumerate(text):
        # Step 1: Extract archive_date from the "Ruminant Science" line
        archive_date_match = archive_date_pattern.search(line)
        if archive_date_match:
            month, year, volume, issue = archive_date_match.groups()
            current_row['archive_date'] = f"{month}-{year}-{volume}-{issue}"
            continue  # Skip this line from being added to the content

        # Step 2: Capture title_1
        title_1_match = title_1_pattern.search(line)
        if title_1_match:
            if found_title_1:
                # Save the previous title's data
                current_row['content'] = content_buffer.strip()
                rows.append(current_row)
                # Reset current_row for new data
                current_row = {
                    'archive_date': current_row['archive_date'],
                    'title': '',
                    'title_2': '',
                    'content': ''
                }
                content_buffer = ''

            # Capture title 1
            current_row['title'] = title_1_match.group(2)
            found_title_1 = True
            continue

        # Step 3: Capture title_2 with Title, Authors, and Source included
        if "Title:" in line and found_title_1:
            # Check the next few lines for Authors: and Source:
            title_2_content = line + "\n"  # Keep '2-Title:'

            # Look ahead for Authors: and Source:
            if i + 1 < len(text) and authors_pattern.search(text[i + 1]):
                title_2_content += text[i + 1] + "\n"
            if i + 2 < len(text) and source_pattern.search(text[i + 2]):
                title_2_content += text[i + 2] + "\n"

            current_row['title_2'] = title_2_content.strip()

        # Step 4: Capture all content, including the title_2 content
        if not title_1_match and not archive_date_match:
            content_buffer += line + "\n"

    # Save the last row
    if found_title_1:
        current_row['content'] = content_buffer.strip()
        rows.append(current_row)

    return rows

# Function to export parsed data to a CSV file
def export_to_csv(data, output_file):
    fieldnames = ['archive_date', 'title', 'title_2', 'content']
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
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
input_file = '/mnt/data/output_file.docx'  # Path to the input .docx file
output_file = '/mnt/data/final_extracted_output.csv'  # Path to save the CSV file
docx_to_csv(input_file, output_file)

print("CSV extraction with improved title_2 and complete content is done!")
