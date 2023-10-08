import re
import csv
import os
import json


# EXTRACTING PASSAGES FROM THE CORPUS DIRECTORY
def extract_passages(uploaded_file):
    # Extracting passages
    match = re.search(r'(?<=__section__).*', uploaded_file, re.DOTALL)
    if match:
        sections = match.group().strip()
    else:
        print("Section not found!")

    all_passages = []
    paragraphs = re.findall(r'(?:^|__paragraph__\n)(.*?)(?=\n__paragraph__|$)', sections, re.DOTALL)
    all_passages = ''.join(paragraphs).strip()
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(all_passages)

    return all_passages


def split_passages_into_chunks(passage):
    chunks = []
    chunk_length = len(passage) // 5
    for i in range(5):
        start_idx = i * chunk_length
        end_idx = (i + 1) * chunk_length if i != 4 else len(passage)
        chunks.append(passage[start_idx:end_idx])
    return chunks


def extract_metadata(uploaded_metadata):
    metadata = json.loads(uploaded_metadata)
    return metadata


def save_passage_metadata(meta, passage_chunks):
    output = []
    for chunk in passage_chunks:
        output.append((chunk, json.dumps(meta)))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "..", "docs")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Append numbers to filenames if the name already exists
    base_name = 'passage_metadata_emb'
    extension = '.csv'
    counter = 1
    output_path = os.path.join(output_dir, base_name + extension)

    # Check if file exists and modify filename if it does
    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f"{base_name}_{counter}{extension}")
        counter += 1

    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Passage', 'Metadata'])
        writer.writerows(output)

    return output_path
