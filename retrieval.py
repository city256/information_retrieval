import os
import re
from collections import defaultdict
import math

doc_len = defaultdict(lambda: defaultdict(int))

def preprocess(document):
    document = re.sub(r'[^a-zA-Z\s]', '', document)
    document = document.upper()
    tokens = document.split()
    return tokens

def build_index(directory):
    index = defaultdict(lambda: defaultdict(int))
    for filename in os.listdir(directory):
        if filename.encode("UTF-8"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
                document = f.read()
                tokens = preprocess(document)
                doc_len[filename] = len(tokens)
                for token in tokens:
                    index[token][filename] += 1
    return index

def boolean_OR(index, term1, term2):
    return index[term1].keys() | index[term2].keys()

def boolean_AND(index, term1, term2):
    return index[term1].keys() & index[term2].keys()

def boolean_NOT(index, term, directory):
    all_files = {file for file in os.listdir(directory) if file.encode("UTF-8")}
    return all_files - index[term].keys()

def boolean_AND_NOT(index, term1, term2):
    return index[term1].keys() - index[term2].keys()

def boolean_OR_NOT(index, term1, term2):
    return index[term1].keys() | boolean_NOT(index, term2, 'stories')


def ranked_retrieval(index, query, directory):
    scores = defaultdict(int)
    total_term_count = 0
    for term in preprocess(query):
        preprocessed_content = preprocess(query)
        terms = preprocessed_content
        total_term_count += len(terms)

        for document in index[term].keys():
            scores[document] += tf_idf(index, term, document, directory, total_term_count)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def tf_idf(index, term, document, directory, num):

    tf = math.log(1+index[term][document]/doc_len[document])
    idf = math.log(len(os.listdir(directory)) / len(index[term]))
    #print('tf=',tf,', idf=',idf,'tf-idf=',tf*idf, 'term=',term, 'num=',index[term][document],'/',doc_len[document],'document=',document)
    return tf * idf


def main():
    directory = 'stories'
    index = build_index(directory)
    for word, files in index.items():
        print(f"{word}: {', '.join([f'{file}:{count}' for file, count in files.items()])}")

    # Report statistics
    num_documents = len({file for file in os.listdir(directory) if file.encode("UTF-8")})
    num_terms = len(index)
    avg_terms_per_document = sum(len(tokens) for tokens in index.values()) / num_documents
    max_terms_in_document = max(len(tokens) for tokens in index.values())
    min_terms_in_document = min(len(tokens) for tokens in index.values())
    most_common_term = max(index.items(), key=lambda x: len(x[1]))

    print("Index statistics:")
    print(f"Total number of documents: {num_documents}")
    print(f"Total number of unique terms: {num_terms}")
    print(f"Average number of terms per document: {avg_terms_per_document}")
    print(f"Maximum number of terms in a document: {max_terms_in_document}")
    print(f"Minimum number of terms in a document: {min_terms_in_document}")
    print(f"Term that appears in the most documents: {most_common_term[0]} ({len(most_common_term[1])} documents)")

    # Boolean retrieval
    print("Boolean retrieval:")
    print("X OR Y:", boolean_OR(index, "X", "Y"))
    print("X AND Y:", boolean_AND(index, "X", "Y"))
    print("X AND NOT Y:", boolean_AND_NOT(index, "X", "Y"))
    print("X OR NOT Y:", boolean_OR_NOT(index, "X", "Y"))

    # Ranked retrieval
    print("\nRanked retrieval:")
    query = input('input free text query : ')

    print("Query:",query)
    print(ranked_retrieval(index, query, directory))
if __name__ == "__main__":
    main()

