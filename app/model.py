import csv
import os.path
from sentence_transformers import SentenceTransformer
import json


def passage_emb(chunks, metadata):
    model = SentenceTransformer('all-mpnet-base-v2')
    embeddings = model.encode(chunks)

    output_data = [(chunk, metadata, json.dumps(embedding.tolist())) for chunk, embedding in zip(chunks, embeddings)]

    # SAVING THE FILE INTO CSV SKIRMISHES
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, '..', 'docs')

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
        writer.writerow(['Passage', 'Metadata', 'Embedding'])
        writer.writerows(output_data)

    return writer
