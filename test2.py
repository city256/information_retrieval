import os
import re
from collections import defaultdict
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

def build_index(directory):
    index = defaultdict(set)
    for filename in os.listdir(directory):
        words = preprocess(os.path.join(directory, filename))
        for word in words:
            index[word].add(filename)
    return index

import os

def load_dataset(directory):
    dataset = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):  # check if it is a file
            with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:  # errors='ignore' to handle potential encoding issues
                dataset[filename] = f.read()
    return dataset

dataset = load_dataset('stories')

def preprocess_dataset(dataset):
    preprocessed_dataset = {}
    for filename, content in dataset.items():
        preprocessed_dataset[filename] = preprocess(content)
    return preprocessed_dataset

def build_index(preprocessed_dataset):
    index = defaultdict(set)
    for filename, words in preprocessed_dataset.items():
        for word in words:
            index[word].add(filename)
    return index

preprocessed_dataset = preprocess_dataset(dataset)
index = build_index(preprocessed_dataset)
