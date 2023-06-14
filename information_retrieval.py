import re
from collections import defaultdict

def preprocess(text):
    # Remove punctuations and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    # Normalize to lowercase
    text = text.lower()

    # Perform stemming (optional)
    # stemmer = YourStemmer()
    # text = stemmer.stem(text)

    return text


def build_inverted_index(dataset):
    inverted_index = defaultdict(list)

    for doc_id, document in enumerate(dataset):
        preprocessed_doc = preprocess(document)
        terms = preprocessed_doc.split()

        for term in set(terms):
            inverted_index[term].append(doc_id)

    return inverted_index


# Load dataset
dataset = []
with open('stories/game.txt', 'r') as file:
    dataset = file.readlines()

# Build inverted index
inverted_index = build_inverted_index(dataset)

# Print the inverted index
for term, postings in inverted_index.items():
    print(f'{term}: {postings}')

def boolean_retrieval(query, inverted_index):
    query_terms = query.split()
    result = None
    operator = None

    for term in query_terms:
        if term == 'AND':
            operator = 'AND'
            continue
        elif term == 'OR':
            operator = 'OR'
            continue
        elif term == 'NOT':
            operator = 'NOT'
            continue

        term = preprocess(term)
        term_postings = set(inverted_index.get(term, []))

        if operator == 'AND':
            result = result.intersection(term_postings) if result else term_postings
        elif operator == 'OR':
            result = result.union(term_postings) if result else term_postings
        elif operator == 'NOT':
            result = result.difference(term_postings) if result else set()
        else:
            result = term_postings

    return result


def boolean_retrieval(query, inverted_index):
    query_terms = query.split()
    result = None
    operator = None

    for term in query_terms:
        if term == 'AND':
            operator = 'AND'
            continue
        elif term == 'OR':
            operator = 'OR'
            continue
        elif term == 'NOT':
            operator = 'NOT'
            continue
        elif term == 'NAND':
            operator = 'NAND'
            continue
        elif term == 'NOR':
            operator = 'NOR'
            continue

        term = preprocess(term)
        term_postings = set(inverted_index.get(term, []))

        if operator == 'AND':
            result = result.intersection(term_postings) if result else term_postings
        elif operator == 'OR':
            result = result.union(term_postings) if result else term_postings
        elif operator == 'NOR':
            result = result.difference(term_postings) if result else set()
        elif operator == 'NAND':
            result = set(range(max(inverted_index.values())[0] + 1)).difference(term_postings)
        else:
            result = term_postings

    return result

# Example usage

query = 'around OR of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')
query = 'around AND of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')
query = 'around NAND of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')
query = 'around NOR of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')

import math
def calculate_tf_idf(tf, idf):
    return tf * idf

def ranked_retrieval(query, inverted_index, dataset):
    query_terms = preprocess(query).split()
    scores = defaultdict(float)

    # Calculate query term frequencies
    query_tf = defaultdict(int)
    for term in query_terms:
        query_tf[term] += 1

    # Calculate inverse document frequencies
    N = len(dataset)
    query_idf = {}
    for term in query_terms:
        df = len(inverted_index.get(term, []))
        idf = math.log(N / (df + 1))  # Add smoothing to avoid division by zero
        query_idf[term] = idf

    # Calculate document scores using TAAT
    for doc_id in range(N):
        doc_terms = preprocess(dataset[doc_id]).split()

        for term in query_terms:
            tf = doc_terms.count(term)
            idf = query_idf[term]
            tf_idf = calculate_tf_idf(tf, idf)

            scores[doc_id] += tf_idf

    # Sort documents by score in descending order
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ranked_doc_ids = [doc_id for doc_id, _ in ranked_docs]

    return ranked_doc_ids

# Example usage
query = 'hi'
results = ranked_retrieval(query, inverted_index, dataset)
print(f'Results for query "{query}": {sorted(results)}')
