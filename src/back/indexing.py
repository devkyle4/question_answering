import hashlib
import os.path
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import csv

load_dotenv()

es_port = os.environ.get("ES_PORT")
es_host = os.environ.get("ES_HOST")


def get_es():
    es = Elasticsearch(
        hosts=[{"host": es_host, "port": es_port, "scheme": "http"}],
        basic_auth=("devkyle", "123456"),
    )
    return es


# Define the mapping
mapping = {
    "mappings": {
        "properties": {
            "Passage": {"type": "text"},
            "Metadata": {"type": "text"},
            "Embedding": {"type": "dense_vector", "dims": 768},
        }
    }
}


# Create index with the mapping
def create_index(index_name, the_mapping):
    es = get_es()
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=the_mapping)
        print("Index Created")
    else:
        print("Index already created!!")


def generate_unique_id(passage, metadata):
    """Generate a unique hash using the combination of passage and metadata."""
    return hashlib.md5((passage + metadata).encode("utf-8")).hexdigest()


def index_data_from_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        actions = []
        for row in reader:
            passage, metadata, embedding = row
            embedding = list(map(float, embedding.strip("[]").split(",")))

            # Use the unique ID for the document
            doc_id = generate_unique_id(passage, metadata)

            action = {
                "_op_type": "index",
                "_index": "legal_passages",
                "_id": doc_id,  # Add this unique ID here
                "_source": {
                    "Passage": passage,
                    "Metadata": metadata,
                    "Embedding": embedding,
                },
            }
            actions.append(action)
        helpers.bulk(get_es(), actions)
