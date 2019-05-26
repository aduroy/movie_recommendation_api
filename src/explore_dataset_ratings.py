import pandas as pd
from ascii_graph import Pyasciigraph

pd.options.display.width = None
pd.set_option('display.max_columns', None)


def title(t):
    return '# ---------- {} ---------- #'.format(t)


def subtitle(st):
    return '\n=> {}:'.format(st)


def subtitle2(st, new_line=True):
    return '{}- {}:'.format('\n' if new_line else '', st)

# -----------------------------------------------------------------------------
# ratings.csv
# -----------------------------------------------------------------------------
print(title('ratings.csv'))

print('Loading csv...')
ratings = pd.read_csv('data/ratings.csv')
print('Done!')

print(subtitle('GENERAL'))

print(subtitle2('Nb users', new_line=False))
print(ratings['userId'].unique().shape[0])
print(subtitle2('Nb movies'))
print(ratings['movieId'].unique().shape[0])

print(subtitle('USERS'))

users_votes = ratings.groupby('userId').size()
print(subtitle2('Nb votes for users', new_line=False))
print('Min.   {}'.format(users_votes.min()))
print('Max.   {}'.format(users_votes.max()))
print('Avg    {}'.format(round(users_votes.mean(), 2)))
print('Median {}'.format(users_votes.median()))
print('Std    {}'.format(round(users_votes.std(), 2)))

print(subtitle2('Top 5 users (#votes):'))
print(users_votes.to_frame('nb_votes').sort_values('nb_votes', ascending=False)[:5])

print(subtitle2('Flop 5 users (#votes):'))
print(users_votes.to_frame('nb_votes').sort_values('nb_votes', ascending=True)[:5])

print(subtitle('MOVIES'))

movies = pd.read_csv('data/movies.csv')

movies_votes_card = ratings.groupby('movieId').size()
print(subtitle2('Nb votes for movies', new_line=False))
print('Min.   {}'.format(movies_votes_card.min()))
print('Max.   {}'.format(movies_votes_card.max()))
print('Avg    {}'.format(round(movies_votes_card.mean(), 2)))
print('Median {}'.format(movies_votes_card.median()))
print('Std    {}'.format(round(movies_votes_card.std(), 2)))

print(subtitle2('Top 5 movies (#votes):'))
mv = movies_votes_card.to_frame('nb_votes')
mv = mv.sort_values('nb_votes', ascending=False)[:5]
print(mv.join(movies.set_index('movieId'))[:5])

print(subtitle2('Flop 5 movies (#votes):'))
mv = movies_votes_card.to_frame('nb_votes')
mv = mv.sort_values('nb_votes', ascending=True)[:5]
print(mv.join(movies.set_index('movieId'))[:5])

movies_votes_avg = ratings.groupby('movieId')['rating'].mean()
print(subtitle2('Top 5 movies (avg. score):'))
mv = movies_votes_avg.to_frame('avg_score')
mv = mv.sort_values('avg_score', ascending=False)[:5]
print(mv.join(movies.set_index('movieId'))[:5])


print(subtitle2('Flop 5 movies (avg. score):'))
mv = movies_votes_avg.to_frame('avg_score')
mv = mv.sort_values('avg_score', ascending=True)[:5]
print(mv.join(movies.set_index('movieId'))[:5])

print(subtitle('RATINGS'))

print(subtitle2('Nb ratings', new_line=False))
print(len(ratings.index))

print(subtitle2('Ratings (values)'))
print('Min.   {}'.format(ratings['rating'].min()))
print('Max.   {}'.format(ratings['rating'].max()))
print('Avg    {}'.format(round(ratings['rating'].mean(), 2)))
print('Median {}'.format(ratings['rating'].median()))
print('Std    {}'.format(round(ratings['rating'].std(), 2)))

print(subtitle('Ratings distribution'))
ratings_distrib = ratings['rating'].value_counts().sort_index(ascending=False)
print(ratings_distrib)
graph = Pyasciigraph()
data = [(val, cnt) for val, cnt in ratings_distrib.iteritems()]
for line in graph.graph(subtitle('Ratings distribution'), data):
    print(line)
