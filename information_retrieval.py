
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
#print(inverted_index)
print('Number of Terms :',len(inverted_index))

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
        elif term == 'AND_NOT':
            operator = 'AND_NOT'
            continue
        elif term == 'OR_NOT':
            operator = 'OR_NOT'
            continue

        term = preprocess(term)
        term_postings = set(inverted_index.get(term, []))

        if operator == 'AND':
            result = result.intersection(term_postings) if result else term_postings
        elif operator == 'OR':
            result = result.union(term_postings) if result else term_postings
        elif operator == 'OR_NOT':
            result = result.difference(term_postings) if result else set()
        elif operator == 'AND_NOT':
            result = set(range(max(inverted_index.values())[0] + 1)).difference(term_postings)
        else:
            result = term_postings

    return result

query = 'around AND of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')
query = 'around OR of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')
query = 'around AND_NOT of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')
query = 'around OR_NOT of'
print(f'Documents satisfying the query "{query}": {sorted(boolean_retrieval(query, inverted_index))}')


