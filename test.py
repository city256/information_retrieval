
import requests
import zipfile
import io

r = requests.get('http://archives.textfiles.com/stories.zip')
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

import os
import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def preprocess(file):
    with open(file, 'r') as f:
        text = f.read()
    text = re.sub('[^a-zA-Z]', ' ', text)  # remove punctuation and numbers
    text = text.upper()  # convert to upper case
    words = text.split()
    words = [ps.stem(word) for word in words]  # optional stemming
    return words

from collections import defaultdict

def build_index(directory):
    index = defaultdict(set)
    for filename in os.listdir(directory):
        words = preprocess(os.path.join(directory, filename))
        for word in words:
            index[word].add(filename)
    return index

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




def calculate_index_statistics(inverted_index):
    total_terms = 0
    unique_terms = len(inverted_index)
    total_documents = set()
    max_term_frequency = 0
    min_term_frequency = float('inf')
    total_term_frequency = 0

    for term, postings in inverted_index.items():
        term_frequency = len(postings)
        total_terms += term_frequency
        total_term_frequency += term_frequency

        if term_frequency > max_term_frequency:
            max_term_frequency = term_frequency

        if term_frequency < min_term_frequency:
            min_term_frequency = term_frequency

        for doc_id in postings:
            total_documents.add(doc_id)

    number_of_documents = len(total_documents)
    average_term_frequency = total_terms / number_of_documents
    average_document_length = total_terms / len(inverted_index)

    return unique_terms, number_of_documents, average_term_frequency, max_term_frequency, min_term_frequency, average_document_length, total_terms

# Calculate index statistics
unique_terms, number_of_documents, average_term_frequency, max_term_frequency, min_term_frequency, average_document_length, total_terms = calculate_index_statistics(inverted_index)

# Print index statistics
print("Index Statistics:")
print(f"Number of Unique Terms: {unique_terms}")
print(f"Number of Documents: {number_of_documents}")
print(f"Average Term Frequency per Document: {average_term_frequency:.2f}")
print(f"Maximum Term Frequency per Document: {max_term_frequency}")
print(f"Minimum Term Frequency per Document: {min_term_frequency}")
print(f"Average Document Length: {average_document_length:.2f}")
print(f"Total Number of Terms: {total_terms}")
