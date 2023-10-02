import os.path
from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
    basic_auth=(username, password)
)

INDEX_NAME = 'legal_passages'

# Define the mapping
mapping = {
    "mappings": {
        "properties": {
            "Passage": {
                "type": "text"
            },
            "Metadata": {
                "type": "text"
            },
            "Embedding": {
                "type": "dense_vector",
                "dims": 768
            }
        }
    }
}


# Create index with the mapping
def create_index(index_name, the_mapping):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=the_mapping)


# Storing data from CSV file to ElasticSearch
def index_data_from_csv(filepath):
    # filepath = path to csv file of the passage, metadata and embeddings
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        actions = []
        for row in reader:
            passage, metadata, embedding = row
            embedding = list(map(float, embedding.strip('[]').split(',')))

            action = {
                "_index": INDEX_NAME,
                "_source": {
                    "Passage": passage,
                    "Metadata": metadata,
                    "Embedding": embedding
                }
            }
            actions.append(action)
        helpers.bulk(es, actions)


current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = os.path.join(current_dir, '..', 'docs')
file_path = os.path.join(current_dir, file_dir, 'passage_metadata_emb.csv')

create_index(INDEX_NAME, mapping)
index_data_from_csv(file_path)
