from collections import defaultdict

from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime


class SpacyEmbedding(BaseEstimator, TransformerMixin):
    def __init__(self, spacy):
        self.spacy = spacy

    def fit(self, X, y):
        return self

    def transform(self, documents):
        vecs = []
        for document in documents:
            doc = self.spacy(document)

            vecs.append(doc.vector)
        return vecs


class WordEmbedding(BaseEstimator, TransformerMixin):
    """
    http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
    """

    def __init__(self):
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format(
            'data/embeddings/GoogleNews-vectors-negative300.bin', binary=True)
        self.word2weight = None
        self.dim = 300
        print('{} embedding loaded'.format(str(datetime.now())))

    def fit(self, X, y):
        # tfidf = TfidfVectorizer(analyzer=lambda x: x)
        # tfidf.fit(X)
        # # if a word was never seen - it must be at least as infrequent
        # # as any of the known words - so the default idf is the max of
        # # known idf's
        # max_idf = max(tfidf.idf_)
        # self.word2weight = defaultdict(
        #     lambda: max_idf,
        #     [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w]  # * self.word2weight[w]
                     for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])


class Glove100(BaseEstimator, TransformerMixin):
    """
    http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
    """

    def __init__(self):
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format('data/embeddings/glove.100d.txt', binary=False)
        self.word2weight = None
        self.dim = 100

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                     for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])


class Glove300(BaseEstimator, TransformerMixin):
    """
    http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
    """

    def __init__(self):
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format('data/embeddings/glove.300d.txt', binary=False)
        self.word2weight = None
        self.dim = 300

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                     for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])
