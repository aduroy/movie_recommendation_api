import pandas as pd
import joblib
from surprise import Reader, Dataset, SVD

# -----------------------------------------------------------------------------
# Load 20M dataset
# -----------------------------------------------------------------------------
ratings = pd.read_csv('data/ratings.csv')

reader = Reader()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset = data.build_full_trainset()

algo = SVD()
algo.fit(trainset)

joblib.dump(algo, 'data/model/model_20M.pkl')

