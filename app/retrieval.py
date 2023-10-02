import csv
from indexing import es, INDEX_NAME
from sentence_transformers import SentenceTransformer


#   TAKES QUESTIONS AS INPUT AND CHANGE INTO AN EMBEDDING
def compute_question_embedding(question):
    model = SentenceTransformer('all-mpnet-base-v2')
    question_embedding = model.encode(question)
    return question_embedding


#   RETRIEVING PASSAGES FROM ELASTICSEARCH INDEX
def retrieve_relevant_passages(question_embedding, size=3):
    query = {
        "size": size,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_embedding,'Embedding') + 1.0",
                    "params": {
                        "query_embedding": question_embedding
                    }
                }
            }
        }
    }
    response = es.search(index=INDEX_NAME)
    return response['hits']['hits']


# SAVING QUESTION AND REPLY TO A CSV FILE
def save_to_csv(questions, filename="../docs/questions_answers.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['Question', 'Passage 1', 'Relevance Score 1', 'Passage 1 Metadata',
                         'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata',
                         'Passage 3', 'Relevance Score 3', 'Passage 3 Metadata'])

        for question in questions:
            question_embedding = compute_question_embedding(question)
            results = retrieve_relevant_passages(question_embedding)
            row = [question]
            for hit in results:
                passage = hit['_source']['Passage']
                score = hit['_score']
                metadata = hit['_source']['Metadata']
                row.extend([passage, score, metadata])
            writer.writerow(row)


QUESTION = 'What is the name of the plaintiff?'
QUESTION_EMB = compute_question_embedding(QUESTION)
retrieve_relevant_passages(QUESTION_EMB)