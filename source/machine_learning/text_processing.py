import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

nltk.download('punkt')

# stemming of data
def stem_data(data):
    stemmer = PorterStemmer()
    corpus_stemmed = [" ".join([stemmer.stem(word) for word in doc.split()]) for doc in data]
    return corpus_stemmed

# vectorize data
def vectorize(data, vec_type='tfidf'):
    # tfidf vectorizer reward words which occur often in a particular document but rarely in all documents
    if vec_type == 'tfidf':
        # remove stop words - most common words which are not important for meaning
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(data)
        return tfidf_matrix
    # count vectorizer rewards commonly occuring words
    elif vec_type == 'count':
        countvec = CountVectorizer(stop_words='english')
        countvec_matrix = countvec.fit_transform(data)
        return countvec_matrix
