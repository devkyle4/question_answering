from indexing import create_index, INDEX_NAME, index_data_from_csv
from retrieval import compute_question_embedding, save_to_csv, retrieve_relevant_passages
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask import Flask, request, jsonify, abort, render_template_string
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


@app.route('/ask', methods=['GET'])
def get_question():
    question = request.args.get('question')
    if not question:
        return "Please provide a question with the 'question' query parameter.", 400

    # Get the embedding of the question
    question_embedding = compute_question_embedding(question)

    # Fetch relevant passages
    results = retrieve_relevant_passages(question_embedding)

    # Extract the most relevant passage (you can customize this as needed)
    if results:
        top_result = results[0]['_source']['Passage']
    else:
        top_result = "No relevant passage found for your question."

    # Render the result in a simple HTML response
    template = """
    <h2>Your Question:</h2>
    <p>{{ question }}</p>
    <h2>Answer:</h2>
    <p>{{ answer }}</p>
    """

    return render_template_string(template, question=question, answer=top_result)


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json('what is the name of the plaintiff?')

    # Request validation
    if not data or 'question' not in data:
        abort(400, description="Invalid request. Please send a question.")

    question = data['question']
    question_embedding = compute_question_embedding(question)
    results = retrieve_relevant_passages(question_embedding)

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
    app.run(debug=True)
