from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

from src.user import User
from src.movie import Movie

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/*": {"origins": "*"}})

API_VERSION = 'v1'
ROOT_API = '/api/{}'.format(API_VERSION)


def norm_URI(uri):
    return '{}{}'.format(ROOT_API, uri)


class UserAPI(Resource):

    def get(self, user_id):
        user = User(user_id)
        user_info = user.get_info()

        if user_info is None:
            return {
                'error': 'User [{}] does not exist.'.format(user_id)
            }, 204

        payload = {
            'id': user_id,
            'movies': user_info
        }

        return payload, 200


class SuggestedMoviesAPI(Resource):

    def get(self, user_id):
        user = User(user_id)

        try:
            suggested_movies = user.get_suggested_movies(n=150)
        except Exception:
            return {
                'error': 'User [{}] does not exist.'.format(user_id)
            }, 204

        payload = {
            'suggested_movies': suggested_movies
        }

        return payload, 200


class MovieAPI(Resource):

    def get(self, movie_id):
        movie = Movie(movie_id)

        if not movie.exist:
            return {
                'error': 'Movie [{}] does not exist.'.format(movie_id)
            }, 204

        return movie.to_dict(), 200


class SimilarMoviesAPI(Resource):

    def get(self, movie_id):
        movie = Movie(movie_id)
        similar_movies = movie.get_similar_movies(top=100)

        if similar_movies is None:
            return {
                'error': 'User [{}] does not exist.'.format(movie_id)
            }, 204

        payload = {
            'most_similar_movies': similar_movies
        }

        return payload, 200


api.add_resource(UserAPI,
                 norm_URI('/users/<int:user_id>'),
                 norm_URI('/users/<int:user_id>/'),
                 endpoint='user')
api.add_resource(SuggestedMoviesAPI,
                 norm_URI('/users/<int:user_id>/suggested_movies'),
                 norm_URI('/users/<int:user_id>/suggested_movies/'),
                 endpoint='suggested_movies')
api.add_resource(MovieAPI,
                 norm_URI('/movies/<int:movie_id>'),
                 norm_URI('/movies/<int:movie_id>/'),
                 endpoint='movie')
api.add_resource(SimilarMoviesAPI,
                 norm_URI('/movies/<int:movie_id>/most_similar_movies'),
                 norm_URI('/movies/<int:movie_id>/most_similar_movies/'),
                 endpoint='most_similar_movies')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
