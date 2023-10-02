import csv
import os.path
from sentence_transformers import SentenceTransformer
from parsing import CHUNKS, METADATA
import json


def passage_emb(chunks, metadata):
    model = SentenceTransformer('all-mpnet-base-v2')
    embeddings = model.encode(chunks)

    output_data = [(chunk, metadata, json.dumps(embedding.tolist())) for chunk, embedding in zip(chunks, embeddings)]

    # SAVING THE FILE INTO CSV SKIRMISHES
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, '..', 'docs')
    output_path = os.path.join(current_dir, output_dir, 'passage_metadata_emb.csv')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Passage', 'Metadata', 'Embedding'])
        writer.writerows(output_data)

    return ""
