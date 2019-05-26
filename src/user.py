from src.load_data import ratings, tags, movies, algo
from src.movie import Movie


class User:

    def __init__(self, user_id):
        self.id = user_id

    def get_info(self):
        """
        Get general information about the user:
            - rated movies with their relative genres
        """
        user_ratings = ratings[ratings['userId'] == self.id]
        user_tags = tags[tags['userId'] == self.id]

        if len(user_ratings.index) == 0:
            return None

        user_ratings = user_ratings[['movieId', 'rating']]
        user_tags = user_tags[['movieId', 'tag']]

        user_ratings_tags = user_ratings.join(user_tags.set_index('movieId'), on='movieId', lsuffix='_ratings', rsuffix='_tags')

        user_ratings_tags = user_ratings_tags.groupby('movieId').agg({
            'rating': 'first',
            'tag': lambda x: list(x) if not x.isnull().values.any() else []
        }).rename(
            columns={'tag': 'tags'}
        )

        user_ratings_tags_movies = user_ratings_tags.join(movies.set_index('movieId'))
        user_ratings_tags_movies.reset_index(inplace=True)

        user_info = user_ratings_tags_movies.to_dict(orient='records')
        user_info = sorted(user_info, key=lambda k: k['rating'], reverse=True)

        return user_info

    def get_suggested_movies(self, n):
        """
        Get the top `n` suggested movies for the user:
            - based on 20M ratings
            - model-based collaborative filtering (matrix factorization)
            - using SVD algorithm
        More info at: /src/generate_prediction_model.py
        """
        movie_ids = ratings['movieId'].unique()

        user_ratings = ratings[ratings['userId'] == self.id]
        already_voted_movies = user_ratings['movieId'].tolist()

        predictions = [algo.predict(self.id, movie_id) for movie_id in movie_ids if movie_id not in already_voted_movies]
        predictions = sorted(predictions, key=lambda x: x.est, reverse=True)
        n_predictions = predictions[:n]

        suggested_movies = []
        for prediction in n_predictions:
            movie = Movie(prediction.iid.item())
            suggested_movies.append(dict(movie.to_dict(), estimated_score=round(prediction.est.item(), 3)))

        return suggested_movies

