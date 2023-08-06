import nltk
import string
import os

from ..normalization import NormalizeText
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

class ParseText:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.normalizer = NormalizeText()
        
    def stem_tokens(self, tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens)
        return stems

    def process_text(self, text):
        text = text.lower()
        return " ".join(
            [self.normalizer.strip_punctuation(word)
             for word in text.split(" ")]
        )
        
    def tfidf(self, documents):
        documents = [self.process_text(document) for document in documents]
        tfidf_vectorizer = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
        return tfidf_vectorizer.fit_transform(documents)

    
    # to do
    # add text summarization
    # add topic modeling, as well as topic assignment,
    # from a topic model
    # add build your own NER chuncker
    # add build your own POS tagger
    # add some embedding functionality
