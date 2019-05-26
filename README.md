# Movie Recommendation API

This project aims at providing a simple API for movie recommendation, based on:

> MovieLens 20M Dataset

=> [download](https://grouplens.org/datasets/movielens/)

Please save CSV files into the `data/` folder.

The pre-trained model for 20M ratings is downloadable [here](https://we.tl/t-s2o6YaPDgV) and must be placed in `data/model/`.

## Approach

To achieve the task, the following steps are:

    [1] Explore the dataset
    [2] Build a recommender system for any user in the dataset
    [3] Build a similarity measure between movies
    [4] Measure results

[1] Dataset exploration can be found at:

```bash
- results/output_explore_dataset_movies.txt
- results/output_explore_dataset_ratings.txt
```

which are basically outputs of, respectively:

```bash
python src/explore_dataset_movies.py
python src/explore_dataset_ratings.py
```

[2] & [3] Both are provided through API endpoints, see below.

[4] See `Results` section

## Requirements

This project is developed using `python 3.7`.

### Advises

For a better experience, please make sure:

- the right version of `python` is installed
- `pip` is installed
- a `virtualenv` is configured

### Installation

Install dependencies in the root directory:

```bash
pip install -r requirements.txt
```

> NB: Installing the package `scikit-surprise` on `Windows` might require external dependencies, such as Visual Studio C++.

## API setup

The recommendation model is based on a trained model which takes approx. 20 minutes to train. Thus, this is not reasonable to run this task everytime
we restart the server.

For addressing this issue, the model is generated upfront, as follows:

```bash
python src/generate_prediction_model.py
```

The model should be saved to disk at this location:

```bash
data/model/model_20M.pkl
```

> NB: Its size is approx. 875 MB.

Once it is generated, both the `Flask` server and the API can be started using the following command:

```bash
python src/main.py
```

> NB: This may take few minutes (~4-5 min.) since the saved model is loaded into memory at this stage, depending on your configuration.

## API documentation

The API skeleton is the following:

```bash
/api/<API_V>/<ENDPOINT>
```

with

```bash
<API_V>     API version
<ENDPOINT>  One of the following endpoints (without the starting '/')
```

The current API version is: `<API_V> = v1`

### Endpoints

1. GET */users/<USER_ID>*
2. GET */users/<USER_ID>/suggested_movies*
3. GET */movies/<MOVIE_ID>*
4. GET */movies/<MOVIE_ID>/most_similar_movies*

### */users/<USER_ID>*

Get all movies the specified user has rated in the dataset.

e.g.
```bash
GET api/v1/users/96
```

```json
{
    "id": 96,
    "movies": [
        {
            "movieId": 541,
            "rating": 5,
            "tags": [],
            "title": "Blade Runner (1982)",
            "genres": [
                "Action",
                "Sci-Fi",
                "Thriller"
            ]
        },
        {
            "movieId": 5445,
            "rating": 5,
            "tags": [],
            "title": "Minority Report (2002)",
            "genres": [
                "Action",
                "Crime",
                "Mystery",
                "Sci-Fi",
                "Thriller"
            ]
        },
        {
            ...
        }
    ]
}
```

> NB: Result is sorted by `rating`, descending.

### */users/<USER_ID>/suggested_movies*

Get the suggested movies for a specific user, based on his/her previous ratings.

e.g.
```bash
GET api/v1/users/96/suggested_movies
```

```json
{
    "suggested_movies": [
        {
            "id": 77658,
            "title": "Cosmos (1980)",
            "genres": [
                "Documentary"
            ],
            "estimated_score": 4.437
        },
        {
            "id": 92259,
            "title": "Intouchables (2011)",
            "genres": [
                "Comedy",
                "Drama"
            ],
            "estimated_score": 4.269
        },
        {
            "id": 100553,
            "title": "Frozen Planet (2011)",
            "genres": [
                "Documentary"
            ],
            "estimated_score": 4.234
        },
        {
            "id": 104069,
            "title": "Louis C.K.: Oh My God (2013)",
            "genres": [
                "Comedy"
            ],
            "estimated_score": 4.204
        },
        {
            "id": 95858,
            "title": "For the Birds (2000)",
            "genres": [
                "Animation",
                "Children",
                "Comedy"
            ],
            "estimated_score": 4.188
        },
        {
            "id": 1704,
            "title": "Good Will Hunting (1997)",
            "genres": [
                "Drama",
                "Romance"
            ],
            "estimated_score": 4.184
        },
        {
            "id": 91233,
            "title": "Lifted (2006)",
            "genres": [
                "Animation",
                "Comedy",
                "Sci-Fi"
            ],
            "estimated_score": 4.179
        },
        {
            "id": 59387,
            "title": "Fall, The (2006)",
            "genres": [
                "Adventure",
                "Drama",
                "Fantasy"
            ],
            "estimated_score": 4.167
        },
        {
            ...
        }
    ]
}
```

> NB: Result is sorted by `estimated_score`, descending and limited to 150 movies.

### */movies/<MOVIE_ID>*

Get information for a specific movie in the dataset.

e.g.
```bash
GET api/v1/movies/1
```

```json
{
    "id": 1,
    "title": "Toy Story (1995)",
    "genres": [
        "Adventure",
        "Animation",
        "Children",
        "Comedy",
        "Fantasy"
    ]
}
```

### */movies/<MOVIE_ID>/most_similar_movies*

Get the 100 most similar movies to the given one, within the dataset.

e.g.
```bash
GET api/v1/movies/1/most_similar_movies
```

```json
{
    "most_similar_movies": [
        {
            "id": 11872,
            "title": "Shrek the Third (2007)",
            "genres": [
                "Adventure",
                "Animation",
                "Children",
                "Comedy",
                "Fantasy"
            ],
            "cosine_similarity": 1
        },
        {
            "id": 24850,
            "title": "The Magic Crystal (2011)",
            "genres": [
                "Adventure",
                "Animation",
                "Children",
                "Comedy",
                "Fantasy"
            ],
            "cosine_similarity": 1
        },
        {
            "id": 18275,
            "title": "Asterix and the Vikings (Astérix et les Vikings) (2006)",
            "genres": [
                "Adventure",
                "Animation",
                "Children",
                "Comedy",
                "Fantasy"
            ],
            "cosine_similarity": 1
        },
        {
            "id": 10115,
            "title": "DuckTales: The Movie - Treasure of the Lost Lamp (1990)",
            "genres": [
                "Adventure",
                "Animation",
                "Children",
                "Comedy",
                "Fantasy"
            ],
            "cosine_similarity": 1
        },
        {
            "id": 24461,
            "title": "Toy Story Toons: Small Fry (2011)",
            "genres": [
                "Adventure",
                "Animation",
                "Children",
                "Comedy",
                "Fantasy"
            ],
            "cosine_similarity": 1
        },
        {
            ...
        }
    ]
}
        
```

> NB: Result is sorted by `cosine_similarity`, descending and limited to 100 movies.

## Results

Results about predictions results are available in the `results` subdirectory:

    - performance_SVD_100k.txt
    - performance_SVD_1M.txt
    - performance_SVD_20M.txt

They all refer to evaluations of the trained models, on different datasets, using:

    - 5-fold cross validation
    - RMSE as metric
    - SVD as algorithm
    

Results for `performance_SVD_20M.txt`:
```bash
                  Fold 1  Fold 2  Fold 3  Fold 4  Fold 5  Mean    Std
RMSE (testset)    0.7865  0.7859  0.7855  0.7866  0.7860  0.7861  0.0004
Fit time          1040.61 1073.26 1072.87 1096.64 1095.36 1075.75 20.35
Test time         415.78  269.28  260.02  366.01  317.58  325.73  58.82
```

> NB: Note it took approx. 2h to run the cross-validation with my configuration.

### Machine specifications

    - MacBook Air 13"
    - 8 GB 1600 MHz DDR3
    - 2.2 GHz Intel Core i7

### Future development/Improvements

- Most Similar Movies: Use other features than only movie genres
    - tags
    - scrape webpages to get additional info (director, casting, etc)
    - try different clustering techniques
    - get extra tags from content itself (poster, etc)
- Recommended movies:
    - try [neural networks](https://nbviewer.jupyter.org/github/khanhnamle1994/movielens/blob/master/Deep_Learning_Model.ipynb)
    - get more information about the users
    - use timestamp
    - use genome tags
- API
    - handle errors better (proper errors, logs, etc)
    - monitor VM performance
    - secure the API with [JWT](https://pythonhosted.org/Flask-JWT/)
- Use a database instead of CSV files
- Build an Web interface