import pandas as pd
import numpy as np
import itertools

from collections import Counter

from ascii_graph import Pyasciigraph

pd.options.display.width = None
pd.set_option('display.max_columns', None)


def title(t):
    return '# ---------- {} ---------- #'.format(t)


def subtitle(st):
    return '\n=> {}:'.format(st)


def subtitle2(st, new_line=True):
    return '{}- {}:'.format('\n' if new_line else '', st)


def find_year(title):
    title = title.strip()
    year = title[-5:-1]

    if not year.isdigit():
        return None

    return int(year)


# -----------------------------------------------------------------------------
# movies.csv
# -----------------------------------------------------------------------------
print(title('movies.csv'))

print('Loading csv...')
movies = pd.read_csv('data/movies.csv')
print('Done!')

movies['genres'] = movies['genres'].apply(lambda x: sorted(x.split('|')))
movies['year'] = movies['title'].apply(lambda x: find_year(x))

print(subtitle('MOVIES'))
print(subtitle2('Nb movies', new_line=False))
print(len(movies.index))

nb_genres = movies['genres'].apply(lambda x: len(x))
print(subtitle2('Nb genres per movie'))
print('Min.   {}'.format(nb_genres.min()))
print('Max.   {}'.format(nb_genres.max()))
print('Avg    {}'.format(round(nb_genres.mean(), 2)))
print('Median {}'.format(int(nb_genres.median())))
print('Std    {}'.format(round(nb_genres.std(), 2)))


graph = Pyasciigraph()
data = [(val, cnt) for val, cnt in nb_genres.value_counts().iteritems()]
for line in graph.graph(subtitle('Nb genres/movie distribution'), data):
    print(line)

print(subtitle('YEARS'))
print(subtitle2('Years (values)', new_line=False))
print('Min.   {}'.format(int(movies['year'].min())))
print('Max.   {}'.format(int(movies['year'].max())))
print('Avg    {}'.format(round(movies['year'].mean(), 2)))
print('Median {}'.format(int(movies['year'].median())))
print('Std    {}'.format(round(movies['year'].std(), 2)))

print(subtitle('Years distribution'))
years_distrib = movies['year'].value_counts().sort_index(ascending=False)
graph = Pyasciigraph()
data = [(int(val), cnt) for val, cnt in years_distrib.iteritems()]
for line in graph.graph(subtitle('Years distribution'), data):
    print(line)

print(subtitle('GENRES'))
print(subtitle2('Genres', new_line=False))
all_genres = Counter([item for sublist in movies['genres'].tolist() for item in sublist])
graph = Pyasciigraph()
data = [(val, cnt) for val, cnt in all_genres.most_common()]
for line in graph.graph(subtitle('Genres distribution'), data):
    print(line)

print(subtitle2('Co-occurring genres'))
movies['cooc_genres'] = movies['genres'].apply(lambda x: list(itertools.combinations(x, 2)))

all_cooc_genres = np.asarray(movies['cooc_genres'].tolist()).flatten()
all_cooc_genres = Counter([item for sublist in all_cooc_genres for item in sublist])
graph = Pyasciigraph()
data = [('_'.join(val), cnt) for val, cnt in all_cooc_genres.most_common()]
for line in graph.graph(subtitle('Co-occurring genres distribution'), data):
    print(line)