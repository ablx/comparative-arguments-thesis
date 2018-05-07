from sklearn.base import TransformerMixin, BaseEstimator
import re
import numpy as np


def process(text, a, b, mode=None, rep_a='OBJECT_A', rep_b='OBJECT_B'):
    if mode == 'remove':
        _a = re.sub(a, '', text, flags=re.IGNORECASE)
        _b = re.sub(b, '', _a, flags=re.IGNORECASE)
        return re.sub('  ', ' ', _b)  # dunno why python adds a space with the regex?
    elif mode == 'replace':
        _a = re.sub(a, 'OBJECT', text, flags=re.IGNORECASE)
        _b = re.sub(b, 'OBJECT', _a, flags=re.IGNORECASE)
        return re.sub('  ', ' ', _b)
    elif mode == 'replace_dist':
        if b not in text:
            first = a
            second = a
        elif a not in text:
            first = b
            second = a
        elif text.index(b) > text.index(a):
            first = a
            second = b
        else:
            first = b
            second = a
        _a = re.sub(first, rep_a, text, flags=re.IGNORECASE)
        _b = re.sub(second, rep_b, _a, flags=re.IGNORECASE)
        return re.sub('  ', ' ', _b)
    return text


class ExtractAnyField(TransformerMixin, BaseEstimator):

    def __init__(self, field, converter=str):
        self.field = field
        self.converter = converter

    def transform(self, dataframe):
        results = []
        for index, row in dataframe.iterrows():
            results.append(self.converter(row[self.field]))

        reshape2 = np.array(results).reshape(-1, 1)
        return reshape2

    def fit(self, X, y):
        return self


class ExtractRawSentence(TransformerMixin, BaseEstimator):

    def __init__(self, processing=None,rep_a='OBJECT_A', rep_b='OBJECT_B'):
        self.processing = processing
        self.rep_a = rep_a
        self.rep_b = rep_b

    def transform(self, dataframe):
        results = []
        for index, row in dataframe.iterrows():
            results.append(process(row['sentence'], row['object_a'], row['object_b'], self.processing,rep_a=self.rep_a, rep_b=self.rep_b))

        return results

    def fit(self, X, y):
        return self

    def get_feature_names(self):
        return 'FullExtractor'


class ExtractFirstPart(TransformerMixin, BaseEstimator):
    """returns all words before the first object"""

    def __init__(self, processing=None):
        self.processing = processing

    def transform(self, dataframe):
        results = []
        for index, row in dataframe.iterrows():
            a, b, text = row['object_a'], row['object_b'], row['sentence']
            a_index, b_index = text.index(a), text.index(b)
            if a_index < b_index:
                begin, end = a_index + len(a), b_index
            else:
                begin, end = b_index + len(b), a_index
            res = process(str(text[:begin]), a, b, self.processing)
            results.append(res)
        return results

    def fit(self, X, y):
        return self

    def get_feature_names(self):
        return 'FirstExtractor'


class ExtractLastPart(TransformerMixin, BaseEstimator):
    """returns all words after the second object"""

    def __init__(self, processing=None):
        self.processing = processing

    def transform(self, dataframe):
        results = []
        for index, row in dataframe.iterrows():
            a, b, text = row['object_a'], row['object_b'], row['sentence']
            if text.index(a) > text.index(b):
                res = a + text.split(a)[-1]
            else:
                res = b + text.split(b)[-1]
            results.append(process(res, a, b, self.processing))
        return results

    def fit(self, X, y):
        return self

    def get_feature_names(self):
        return 'LastExtractor'


class ExtractMiddlePart(TransformerMixin, BaseEstimator):
    """returns all words between the first and the second object"""

    def __init__(self, processing=None,rep_a='OBJECT_A', rep_b='OBJECT_B'):
        self.processing = processing
        self.rep_a = rep_a
        self.rep_b = rep_b

    def transform(self, dataframe):
        results = []
        for index, row in dataframe.iterrows():
            a, b, text = row['object_a'], row['object_b'], row['sentence']
            a_index, b_index = text.index(a), text.index(b)
            if a_index < b_index:
                begin, end = a_index, b_index + len(b)
            else:
                begin, end = b_index, a_index + len(a)
            res = process(text[begin:end], a, b, self.processing,rep_a=self.rep_a,rep_b=self.rep_b)

            results.append(res)

        return results

    def fit(self, X, y):
        return self

    def get_feature_names(self):
        return 'MiddleExtractor'
