import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate


# -----------------------------------------------------------------------------
# Load 100k dataset
# -----------------------------------------------------------------------------
# data = Dataset.load_builtin('ml-100k')

# -----------------------------------------------------------------------------
# Load 1M dataset
# -----------------------------------------------------------------------------
# data = Dataset.load_builtin('ml-1m')

# -----------------------------------------------------------------------------
# Load 20M dataset
# -----------------------------------------------------------------------------
ratings = pd.read_csv('data/ratings.csv')
reader = Reader()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# -----------------------------------------------------------------------------
# Define algorithm
# -----------------------------------------------------------------------------
algo = SVD()

cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)
