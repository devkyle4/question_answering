import csv
import os.path
from sentence_transformers import SentenceTransformer
import json

model_name = "all-mpnet-base-v2"
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), model_name)

# Check if the model exists locally, if not, download and save
if not os.path.exists(model_path):
    model = SentenceTransformer(model_name)
    model.save(model_path)


def passage_emb(chunks, metadata):
    print(f"Number of chunks: {len(chunks)}")

    model = SentenceTransformer(model_path)
    print("Initializing model complete.")

    try:
        print("Starting encoding...")
        embeddings = model.encode(chunks, show_progress_bar=False)
        print("Encoding complete.")

        output_data = [
            (chunk, metadata, json.dumps(embedding.tolist()))
            for chunk, embedding in zip(chunks, embeddings)
        ]
        print("Processed output data.")
    except Exception as e:
        print(f"Exception during encoding or data processing: {e}")
        return None  # Return or raise the exception as per your need

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "../..", "docs")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("Created output directory.")

    base_name = "passage_metadata_emb"
    extension = ".csv"
    counter = 1
    output_path = os.path.join(output_dir, base_name + extension)

    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f"{base_name}_{counter}{extension}")
        counter += 1
        print(f"Adjusted output filename to: {output_path}")

    try:
        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Passage", "Metadata", "Embedding"])
            writer.writerows(output_data)
            print(f"Data saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Exception while writing to file: {e}")
        return None
