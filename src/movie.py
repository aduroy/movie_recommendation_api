from sklearn.metrics.pairwise import linear_kernel

from src.load_data import movies, movies_tfidf_matrix


class Movie:
    """
    A Movie is instantiated according to a `movieId` present in the dataset.
    Also, the index of the movie in `movies` (pandas.DataFrame) can also be used instead,
        then, set `is_index` to True.
    """

    def __init__(self, movie_id, is_index=False):
        self.id = movie_id
        self.title = ''
        self.genres = []

        self.exist = True
        self.__set_info(is_index)

    def __set_info(self, is_index):
        if is_index:
            movie_df = movies.iloc[[self.id-1]]
        else:
            movie_df = movies[movies['movieId'] == self.id]

        if len(movie_df.index) != 1:
            self.exist = False
            return

        movie = movie_df.iloc[0]

        self.title = movie['title']
        self.genres = movie['genres']

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genres': self.genres
        }

    def get_similar_movies(self, top=10):
        """
        Retrieve the `top` most similar movies:
            - based on movie genres (preprocessed using TFxIDF)
            - using cosine similarity
        """
        movie_idx = self.id-1
        cosine_similarities = linear_kernel(movies_tfidf_matrix[movie_idx:movie_idx+1], movies_tfidf_matrix).flatten()
        docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != movie_idx]

        result = []
        for index in docs_indices[:top]:
            score = cosine_similarities[index]
            movie = Movie(index.item()+1, is_index=True)

            movie_data = dict(movie.to_dict(), cosine_similarity=round(score.item(), 2))

            result.append(movie_data)

        return result


