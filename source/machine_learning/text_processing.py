import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

nltk.download('punkt')


def stem_data(data):
    stemmer = PorterStemmer()
    corpus_stemmed = [" ".join([stemmer.stem(word) for word in doc.split()]) for doc in data]
    return corpus_stemmed


def vectorize(data, vec_type='tfidf'):
    if vec_type == 'tfidf':
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(data)
        return tfidf_matrix
    elif vec_type == 'count':
        countvec = CountVectorizer(stop_words='english')
        countvec_matrix = countvec.fit_transform(data)
        return countvec_matrix
