import re
import csv
import os
import json


# EXTRACTING PASSAGES FROM THE CORPUS DIRECTORY
def extract_passages(filepath):
    filename = filepath + 'Technical.txt'

    with open(filename, "r", encoding='utf-8') as file:
        content = file.read()

    # Extracting passages
    match = re.search(r'(?<=__section__).*', content, re.DOTALL)
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
    # print(chunk_length)
    for i in range(5):
        start_idx = i * chunk_length
        end_idx = (i + 1) * chunk_length if i != 4 else len(passage)
        chunks.append(passage[start_idx:end_idx])
    return chunks


def extract_metadata(filepath):
    metadata_file = filepath + 'Metadata.json'

    with open(metadata_file, 'r', encoding='utf-8') as file:
        metadata = json.load(file)
    return metadata


def save_passage_metadata(meta, chnks):
    output = []
    for chunk in chnks:
        output.append((chunk, json.dumps(meta)))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "..", "docs")
    output_path = os.path.join(output_dir, "passage_metadata.csv")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Passage', 'Metadata'])
        writer.writerows(output)

    return ''


FILE_NAME = '../docs/Corpus/kwame-legal-EL-1680770407105_'
PASSAGES = extract_passages(FILE_NAME)
METADATA = extract_metadata(FILE_NAME)
CHUNKS = split_passages_into_chunks(PASSAGES)
