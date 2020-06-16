import numpy as np
import pandas as pd
import math

"""
The following functions can be used to calculate the cluster profile for item based filtering
"""


def get_top_movies(cluster, method, n, anime_data, cluster_data):
    """
    Returns top n animes by calculating the cosine distance between the cluster
    profile and the anime profile.

    Parameter specification:
    cluster: string specifying the cluster
    method: string specifying the method to calculate the cluster profile score
    n: number of recommendations to return
    anime_data: pandas dataframe with anime data
    cluster_data: pandas dataframe with cluster data
    """

    # Retrieve cluster profile
    cluster_profile = get_clusterprofile(cluster, method, anime_data, cluster_data)
    cluster_profile_array = np.array(list(cluster_profile.values()))

    # anime score
    anime_score = {}

    # Create weighted dataframe
    weighted_df = get_weights(anime_data)

    # Iterate through all the indexes
    for index in anime_data.index:

        # Different method for unary and unit weight or IDF
        if method == "unary":

            # Retrieve anime array
            anime_array = np.array([anime_data.loc[index]])

        if method == "unit weight" or method == "IDF":

            # Retrieve anime_array
            anime_array = np.array([weighted_df.loc[index]])

        # Cosine numerator and denominator
        numerator = np.sum(cluster_profile_array * anime_array)
        denominator_cluster = np.sqrt(np.sum(np.square(cluster_profile_array)))
        denominator_anime = np.sqrt(np.sum(np.square(anime_array)))

        # Introduce the anime score into the dictionary
        anime_score[index] = numerator / (denominator_cluster / denominator_anime)

    # Transform the dictionary into a tuple sorted by values
    anime_score = sorted(((value, key) for (key, value) in anime_score.items()), reverse=True)

    # Select only the top n values
    return anime_score[0:n]


def get_clusterprofile(cluster, method, anime_data, cluster_data):
    """
    Returns the cluster profile score based on a dot product of cluster data and
    anime data, calculated differently depending the specified method.

    Parameter specification:
    cluster: string specifying the cluster
    method: string specifying the method to calculate the cluster profile score
    anime_data: pandas dataframe containing the anime - topic binary data
    (default value set as topics data)
    cluster_data: pandas dataframe containing the cluster feedback data (default value
    set as cluster_feedback data)
    """

    # Retrieve topics
    genres = anime_data.columns

    # Apply weights to anime_data
    weighted_df = get_weights(anime_data)

    # Retrieve cluster scores
    cluster_scores = np.array([cluster_data[cluster]])

    # Create cluster_profile dictionaries
    cluster_profile = {}

    # Calculate the cluster profile based on different method
    for genre in genres:

        # Calculate the cluster profile scores depending on the different method
        if method == "unary":

            # Retrieve non weighted topic_scores
            genre_scores = np.array([anime_data[genre]])

            # Calculate the cluster profile scores with a dot product
            cluster_genre = np.sum(genre_scores * cluster_scores)

        if method == "unit weight":

            # Retrieve weighted array for topic_scores
            weighted_genres = np.array([weighted_df[genre]])

            # Calculate the topic score
            cluster_genre = np.sum(cluster_scores * weighted_genres)

        if method == "IDF":

            # Retrieve weighted array for topic_scores
            weighted_genres = np.array([weighted_df[genre]])

            # Calculate IDF score and cluster profiles
            genre_scores = np.array([anime_data[genre]])
            idf_genre = math.log10(len(genre_scores)/np.sum(genre_scores))

            # Calculate the topic score
            cluster_genre = np.sum(cluster_scores * weighted_genres) * idf_genre

        # Add key to cluster profile dictionary
        cluster_profile[genre] = cluster_genre

    return cluster_profile


"""
How would the weights be applied
"""


def get_weights(topic_df):
    """
    Returns dataframe of topic data with weights applied based on the total number
    of topics a anime had (if a anime has 5 topics, then each topic has a
    0.20 weight).

    Parameter specification:
    topic_df: dataframe with all the topic - anime data (default value set
    as topics data)
    """

    # Create dictionary from which to create cluster data
    weighted_topics = []

    # Iterate through rows
    for row in topic_df.index:

        # List of weighted values for each anime
        weighted_values = []

        # Calculate weight
        weight = 1 / np.sum(np.array([topic_df.loc[row]]))

        # Iterate through columns
        for column in topic_df.columns:

            # Calculate the new weighted value
            value = topic_df.loc[row, column] * weight
            weighted_values.append(value)

        # Add weighted values list to weighted topics list
        weighted_topics.append(weighted_values)

    weighted_df = pd.DataFrame(data=weighted_topics, index=topic_df.index, columns=topic_df.columns)

    return weighted_df
