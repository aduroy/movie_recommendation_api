from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd

pd.options.display.width = None
pd.set_option('display.max_columns', None)


def useless_func(x):
    """ Used because TfidfVectorizer takes Strings and apply a tokenizer on it.
    If we already work with lists, this makes sense."""
    return x


# -----------------------------------------------------------------------------
# Load CSV files
# -----------------------------------------------------------------------------
ratings = pd.read_csv('data/ratings.csv')
tags = pd.read_csv('data/tags.csv')

movies = pd.read_csv('data/movies.csv')
movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))

# -----------------------------------------------------------------------------
# Pre-compute a TFxIDF matrix based on movie genres
# -----------------------------------------------------------------------------
docs = movies['genres'].tolist()
tfidf = TfidfVectorizer(
    analyzer='word',
    tokenizer=useless_func,
    preprocessor=useless_func,
    token_pattern=None
)
movies_tfidf_matrix = tfidf.fit_transform(docs)

# -----------------------------------------------------------------------------
# Load pre-trained model
# -----------------------------------------------------------------------------
joblib_file = 'data/model/model_20M.pkl'
algo = joblib.load(joblib_file)