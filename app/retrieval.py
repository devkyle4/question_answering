import csv
import os.path
import random

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


# SAVING QUESTION AND ANSWER TO A CSV FILE
def save_to_csv(question, filename="../docs/questions_answers.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['Question', 'Passage 1', 'Relevance Score 1', 'Passage 1 Metadata',
                         'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata',
                         'Passage 3', 'Relevance Score 3', 'Passage 3 Metadata'])

        question_embedding = compute_question_embedding(question)
        results = retrieve_relevant_passages(question_embedding)
        row = [question]
        for hit in results:
            passage = hit['_source']['Passage']
            score = hit['_score']
            metadata = hit['_source']['Metadata']
            row.extend([passage, score, metadata])
        writer.writerow(row)


# CODE FOR EVALUATION
def evaluation(user_queries, csv_file):
    if os.path.splitext(user_queries)[1].lower() != '.txt':  # checking if file is a text file
        return "Wrong file format! Only .txt allowed"
    with open(user_queries, 'r', newline='', encoding='utf-8') as file:
        questions = [line.strip() for line in file]

    relevant_score_1 = None
    relevant_score_2 = None
    relevant_score_3 = None
    if os.path.exists(csv_file):
        return 'can\'t create a duplicate file'
    # SAVING THE EVALUATION IN evaluation.csv AND evaluation_rated.csv
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([' Question', 'Passage 1', 'Relevance Score 1',
                         'Passage 1 Metadata', 'Is Passage 1 Relevant? (Yes/No)',
                         'Passage 2', 'Relevance Score 2', 'Passage 2 Metadata',
                         'Is Passage 2 Relevant? (Yes/No)', 'Passage 3',
                         'Relevance Score 3', 'Passage 3 Metadata', 'Is Passage 3 Relevant? (Yes/No)'])

        for question in questions:
            question_embedding = compute_question_embedding(question)
            results = retrieve_relevant_passages(question_embedding)
            row = [question]
            for hit in results:
                passage = hit['_source']['Passage']
                score = hit['_score']
                metadata = hit['_source']['Metadata']
                relevant = random.choice(['yes', 'no'])
                row.extend([passage, score, metadata, relevant])
            writer.writerow(row)


# ACCURACY FOR TOP 1 AND TOP 3
def compute_accuracies(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        relevant_count = 0
        total_queries = 0

        for row in reader:
            if row[4].lower() == 'yes':
                relevant_count += 1
            if row[8].lower() == 'yes':
                relevant_count += 1
            if row[12].lower() == 'yes':
                relevant_count += 1

        top1_accuracy = (relevant_count // 1) * 100
        top3_accuracy = (relevant_count // 3) * 100

    performance_path = '../docs/performance.csv'
    if os.path.exists(performance_path):
        return 'file already exists'
    with open(performance_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Top 1 Accuracy', 'Top 3 Accuracy'])
        writer.writerow([top1_accuracy, top3_accuracy])

    return top1_accuracy, top3_accuracy


FILENAME = '../docs/evaluation_rated.csv'
compute_accuracies(FILENAME)

# print(evaluation('../docs/user_queries.txt', FILENAME))
