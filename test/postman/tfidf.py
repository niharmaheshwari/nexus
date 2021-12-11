from __future__ import division
import math
import re
from itertools import chain
from collections import Counter

DEFAULT_TOKENIZER = re.compile(r"\b\w+\b").findall

class Document(object):
    def __init__(self, source_text, tokenizer=None):
        if tokenizer is None: tokenizer = DEFAULT_TOKENIZER
        self.source = source_text
        self.tokens = tokenizer(source_text)
        self.terms = Counter(self.tokens)
        most_frequent_term = self.terms.most_common(1)
        
        if most_frequent_term:
            self.max_term_frequency = self.terms.most_common(1)[0][1]
        else:
            #tokenizer produced no tokens from the source text
            self.max_term_frequency = 0.0
            
    def term_frequency(self, term):
        try:
            return self.terms[term] / self.max_term_frequency
        except ZeroDivisionError:
            return 0.0
            
    
class TFIDFCorpus(object):
    
    """
    Usage:
    
    documents = []
    for filename in list_of_documents:
        with open(filename) as f:
            documents.append(Document(f.read()))
            
    corpus = TFIDFCorpus(documents)
    
    print corpus.tfidf("assassination")
    """
    
    def __init__(self, documents):
        self.documents = documents
        self.compile_idf()
        
    def compile_idf(self):
        self.idf_dict = Counter(chain.from_iterable(document.terms for document in self.documents))
        
    def idf(self, term):
        try:
            return math.log(len(self.documents) / self.idf_dict[term])
        except ZeroDivisionError:
            return 0.0
        
    def tfidf(self, term, document):
        return document.term_frequency(term) * self.idf(term)
