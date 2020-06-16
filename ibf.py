from final_project_v1 import *
import pandas as pd
import numpy as np

item_movies = pd.read_csv("item_movies.csv").set_index("anime_id")
item_series = pd.read_csv("item_series.csv").set_index("anime_id")
user_movies = pd.read_csv("user_movies.csv").set_index("anime_id")
user_series = pd.read_csv("user_series.csv").set_index("anime_id")

# Filter to only include the same animes
item_movies = item_movies.iloc[item_movies.index.isin(user_movies.index)]
item_series = item_series.iloc[item_series.index.isin(user_series.index)]

# Filter to only include movies that have a genre
movies = []
for item in item_movies.index:
    if np.sum(np.array(item_movies.loc[item])) > 0:
        movies.append(item)

series = []
for item in item_series.index:
    if np.sum(np.array(item_series.loc[item])) > 0:
        series.append(item)

item_movies = item_movies.iloc[item_movies.index.isin(movies)]
item_series = item_series.iloc[item_series.index.isin(series)]
user_movies = user_movies.iloc[user_movies.index.isin(movies)]
user_series = user_series.iloc[user_series.index.isin(series)]

# Try one user
recommendations = get_top_movies("1", "unary", 5, item_movies, user_movies)
user1_profile = get_clusterprofile("1", "unary", item_movies, user_movies)

# Create empty dictionary for user profiles
user_movies_profiles = []

# All user profiles for movies
for user in user_movies.columns:
    user_movies_profiles.append(get_clusterprofile(user, "IDF", item_movies, user_movies))

# Use profiles data
user_moviesdf = pd.DataFrame(user_movies_profiles, index=user_movies.columns)

# Create empty list for user series
user_series_profiles = []

# All user profiles for series
for user in user_series.columns:
    user_series_profiles.append(get_clusterprofile(user, "IDF", item_series, user_series))

user_seriesdf = pd.DataFrame(user_series_profiles, index=user_series.columns)

user_moviesdf.to_csv("user_movies_clustering.csv")
user_seriesdf.to_csv("user_series_clustering.csv")
