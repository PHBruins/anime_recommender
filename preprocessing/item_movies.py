import pandas as pd
import dask.dataframe as dd
import anime_cleaned as ac
pd.set_option('display.max_columns', 500)

animelists_cleaned = pd.read_csv("animelists_cleaned.csv")
list_of_users = pd.read_csv('UserList.csv')
users = pd.read_csv("user_list.csv")
anime_movies = ac.anime_movies
anime_series = ac.anime_series

"""
Simplify animelist data to merge with movie and series data
"""

# Drop the columns
animelists = animelists_cleaned.drop(['my_watched_episodes', 'my_start_date', 'my_finish_date',
                                      'my_rewatching', 'my_rewatching_ep', 'my_last_updated', 'my_tags'], axis=1)

# Select 1000 users
name_to_id = list_of_users[['username', 'user_id']][0:1000]

# Merge to select only 1000 users
data_ac = animelists.merge(name_to_id, on=['username']).drop(['username'], axis=1)

"""
Create movie item data
"""

# Merge to get anime data
data_movies = data_ac.merge(anime_movies, on=['anime_id'])

# Drop columns
data_movies = data_movies.drop(['my_status', 'scored_by', 'rank', 'popularity',
                                'members', 'favorites', 'duration_min'], axis=1).rename({'score': 'avg_score_anime'}, axis=1)

list_of_genres = ['Shounen', 'Shoujo', 'Seinen', 'Ecchi', 'Mecha', 'Supernatural',
                  'SliceofLife', 'Action', 'Action', 'Adventure', 'Comedy', 'Drama', 'Magic', 'Romance',
                  'type_ONA', 'type_OVA', 'type_special', 'pg13', 'pg17', '90s', '00s', '10s']

data_movies = data_movies.drop(list_of_genres, axis=1)

# Get the user mean rating
unique_user_ids = data_movies['user_id'].unique()
means = []
for user_ids in unique_user_ids:
    user_mean = data_movies.loc[data_movies['user_id'] == user_ids].mean()
    values = [[user_ids, user_mean['my_score']]]
    means.extend(values)
means = pd.DataFrame(means, columns=['user_id', 'avg_score_user'])
data_movies = data_movies.merge(means, on=['user_id'])

# Dummy list
ratings_movies = []

# Create dummy myscore
for index, row in data_movies.iterrows():
    if row["my_score"] > (row["avg_score_user"] + 1):
        ratings_movies.append(1)
    elif row["my_score"] < (row["avg_score_user"] - 1):
        ratings_movies.append(-1)
    else:
        ratings_movies.append(0)

# Create new column with the dummy ratings
data_movies["rating"] = ratings_movies

# Drop all other columns
data_movies = data_movies.drop(["my_score", "avg_score_anime", "avg_score_user"], axis=1)

# Set animes as the index
item_movies = pd.pivot_table(data_movies, values="rating", index="anime_id", columns="user_id")

# Fill NaNs with 0
item_movies = item_movies.fillna(0)

"""
Create series item data
"""

# Merge anime - user data with anime_series data
data_series = data_ac.merge(anime_series, on=['anime_id'])

# Drop columns
data_series = data_series.drop(list_of_genres, axis=1)
data_series = data_series.drop(["episodes", 'my_status', 'scored_by', 'rank', 'popularity',
                                'members', 'favorites', 'duration_min'], axis=1).rename({'score': 'avg_score_anime'}, axis=1)

# Get the user mean rating
unique_user_ids = data_series['user_id'].unique()
means = []
for user_ids in unique_user_ids:
    user_mean = data_series.loc[data_series['user_id'] == user_ids].mean()
    values = [[user_ids, user_mean['my_score']]]
    means.extend(values)
means = pd.DataFrame(means, columns=['user_id', 'avg_score_user'])
data_series = data_series.merge(means, on=['user_id'])

# Dummy list
ratings_series = []

# Create dummy myscore
for index, row in data_series.iterrows():
    if row["my_score"] > (row["avg_score_user"] + 1):
        ratings_series.append(1)
    elif row["my_score"] < (row["avg_score_user"] - 1):
        ratings_series.append(-1)
    else:
        ratings_series.append(0)

# Create new column with the dummy ratings
data_series["rating"] = ratings_series

# Drop all other columns
data_series = data_series.drop(["my_score", "avg_score_anime", "avg_score_user"], axis=1)

# Set animes as the index
item_series = pd.pivot_table(data_series, values="rating", index="anime_id", columns="user_id")

# Fill NaNs with 0
item_series = item_series.fillna(0)
