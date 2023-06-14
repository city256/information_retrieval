
import re
from collections import defaultdict

def preprocess(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()

    return text


def build_inverted_index(dataset):
    inverted_index = defaultdict(list)

    for doc_id, document in enumerate(dataset):
        preprocessed_doc = preprocess(document)
        terms = preprocessed_doc.split()

        for term in set(terms):
            inverted_index[term].append(doc_id)

    return inverted_index


dataset = []
with open('stories/arctic.txt', 'r') as file:
    dataset = file.readlines()

inverted_index = build_inverted_index(dataset)

for term, postings in inverted_index.items():
    print(f'{term}: {postings}')


import math
from collections import Counter
def calculate_tf(term, document):
    term_count = Counter(document.split())
    return term_count.get(term, 0)

def calculate_idf(term, inverted_index, total_documents):
    doc_freq = len(inverted_index.get(term, []))
    return math.log10(total_documents / (1 + doc_freq))

def calculate_tf_idf(term, document, inverted_index, total_documents):
    tf = calculate_tf(term, document)
    idf = calculate_idf(term, inverted_index, total_documents)
    return tf * idf

def ranked_retrieval(query, dataset, inverted_index):
    query_terms = query.split()
    total_documents = len(dataset)
    document_scores = {}

    for doc_id, document in enumerate(dataset):
        score = 0
        for term in query_terms:
            term = preprocess(term)
            score += calculate_tf_idf(term, document, inverted_index, total_documents)
        if score > 0:
            document_scores[doc_id] = score

    print(document_scores)

    sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    ranked_results = [doc_id for doc_id, score in sorted_documents]
    return ranked_results


query = 'he has many'
results = ranked_retrieval(query, dataset, inverted_index)
print(f'Documents matching the query "{query}": {results}')
