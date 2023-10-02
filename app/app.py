from indexing import create_index, INDEX_NAME, index_data_from_csv
from retrieval import compute_question_embedding, save_to_csv, retrieve_relevant_passages
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask import Flask, request, jsonify, abort, render_template_string
import os
import logging
from werkzeug.utils import secure_filename
from parsing import extract_passages, extract_metadata, split_passages_into_chunks
from model import passage_emb

UPLOAD_FOLDER = 'uploaded_documents'
ALLOWED_EXTENSIONS = {'txt', 'json'}

# Initialize the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


 # @app.route('/upload', methods=['POST'])
# def upload_document():
#     if 'document' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['document']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#
#         # Extract passages and metadata from the uploaded document
#         passages = extract_passages(filepath)
#         metadata = extract_metadata(filepath)
#
#         # Split these passages into chunks
#         chunks = split_passages_into_chunks(passages)
#
#         # Get embeddings for these chunks
#         passage_emb(chunks, metadata)
#
#
#         index_data_from_csv(os.path.join("..", "docs", "passage_metadata_emb.csv"))
#
#         return jsonify({"message": "Document uploaded and indexed successfully!"}), 200
#     else:
#         return jsonify({"error": "File type not allowed"}), 400


if __name__ == "__main__":
    app.run(debug=True)
