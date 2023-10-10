from indexing import create_index, index_data_from_csv, mapping
from retrieval import save_to_csv, document_retrieval
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from parsing import extract_metadata, extract_passages, split_passages_into_chunks, save_passage_metadata
from flask import Flask, request, jsonify
from model import passage_emb
import os
import logging

# Initialize the app
app = Flask(__name__)

# Configuration based on environment
ENV = os.environ.get('ENV', 'development')  # Default to development if no environment variable set

if ENV == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif ENV == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.ProductionConfig')

# Logging Setup
logging.basicConfig(filename='api.log', level=logging.DEBUG)
logger = logging.getLogger()

# Creating the index at the start of the application
# create_index('legal_passages', mapping)


@app.route('/', methods=['POST'])
def get_question():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Fetch relevant passages
    results = document_retrieval(question)

    # Extract the most relevant passage (you can customize this as needed)
    if results:
        top_result = results[0]['_source']['Passage']
        score = results[0]['_score']
    else:
        top_result = "No relevant passage found for your question."
        score = "No relevant score"

    return jsonify({"answer": top_result, "score": score})


@app.route('/', methods=['GET'])
def get():
    return 'Oh Yeah!!'


@app.route('/index', methods=['POST'])
def index_documents():
    try:
        print("Received a request for indexing")

        text_file = request.files.get('text_file')
        metadata_file = request.files.get('metadata_file')

        text_content = text_file.read().decode('utf-8') if text_file else None
        metadata_content = metadata_file.read().decode('utf-8') if metadata_file else None

        passages = extract_passages(text_content)
        metadata = extract_metadata(metadata_content)
        chunks = split_passages_into_chunks(passages)
        passage_metadata_csv = save_passage_metadata(metadata, chunks)
        passage_emb_path = passage_emb(chunks, metadata)

        print(passage_emb_path)

        index_data_from_csv(passage_emb_path)

        return jsonify({"message": "Successfully indexed and saved as csv file!"}), 200

    except Exception as e:
        logger.error(f"Error during indexing: {e}")
        return jsonify({"error": "An error occurred during indexing."}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
