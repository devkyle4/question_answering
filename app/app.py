from indexing import create_index, INDEX_NAME, index_data_from_csv
from retrieval import save_to_csv, document_retrieval
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask import Flask, request, jsonify, abort, render_template_string
from flask_limiter import Limiter
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

# SETTING RATE LIMIT OF REQUESTS
limiter = Limiter(
    app,
    default_limits=["50 per day", "50 per hour", "10 per minute"]
)


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
    else:
        top_result = "No relevant passage found for your question."

    return jsonify({"answer": top_result})


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json('what is the name of the plaintiff?')

    # Request validation
    if not data or 'question' not in data:
        abort(400, description="Invalid request. Please send a question.")

    question = data['question']
    results = document_retrieval(question)

    response = {
        "question": question,
        "answers": [
            {
                "passage": hit['_source']['Passage'],
                "score": hit['_score'],
                "metadata": hit['_source']['Metadata']
            }
            for hit in results
        ]
    }
    logger.info(f"Question: {question}, Results: {response}")

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(port=8080, debug=False)
