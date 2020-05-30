import pandas as pd
pd.set_option('display.max_columns', 500)

# Read datasets
anime_cleaned = pd.read_csv("anime_cleaned.csv")

# Only include animes that have been scored by more than 100 members
anime_cleaned = anime_cleaned[anime_cleaned["scored_by"] >= 100]

# Dummy genre
anime_cleaned["genre"] = anime_cleaned["genre"].apply(lambda d: str(d).replace(' ', ''))
anime_cleaned["genre"] = anime_cleaned["genre"].apply(lambda d: str(d).split(sep=","))
dummies_genre = pd.get_dummies(anime_cleaned["genre"].apply(pd.Series).stack()).sum(level=0)
dummies_genre = dummies_genre[["Shounen", "Shoujo", "Seinen", "Ecchi", "Mecha", "Supernatural", "SliceofLife", "Action", "Adventure",
                               "Comedy", "Drama", "Magic", "Romance"]]
anime_cleaned = pd.concat([anime_cleaned, dummies_genre], axis=1)

# Dummy type
dummy_type = pd.get_dummies(anime_cleaned['type'])
anime_cleaned = pd.concat([anime_cleaned, dummy_type], axis=1)
anime_cleaned = anime_cleaned.rename(columns={"Movie": "type_movie", "Music": "type_music",
                                              "ONA": "type_ONA", "OVA": "type_OVA", "Special": "type_special", "TV": "type_TV"})

# Dummy age rating
dummy_rating = pd.get_dummies(anime_cleaned['rating'])
anime_cleaned = pd.concat([anime_cleaned, dummy_rating], axis=1)

all_ages = []
pg13 = []
pg17 = []

for rating in dummy_rating.columns:
    for x in range(len(anime_cleaned)):
        if rating in ["G - All Ages", "PG - Children"]:
            if anime_cleaned[rating].iloc[x] == 1:
                all_ages.append(1)
                pg13.append(0)
                pg17.append(0)
        elif rating in ["PG-13 - Teens 13 or older"]:
            if anime_cleaned[rating].iloc[x] == 1:
                all_ages.append(0)
                pg13.append(1)
                pg17.append(0)
        elif rating in ["R - 17+ (violence & profanity)", "R+ - Mild Nudity", "Rx - Hentai"]:
            if anime_cleaned[rating].iloc[x] == 1:
                all_ages.append(0)
                pg13.append(0)
                pg17.append(1)
        elif rating == "None":
            if anime_cleaned[rating].iloc[x] == 1:
                all_ages.append(0)
                pg13.append(0)
                pg17.append(0)

#anime_cleaned["all_ages"] = all_ages
anime_cleaned["pg13"] = pg13
anime_cleaned["pg17"] = pg17

# Aired dummy
anime_cleaned["90s"] = anime_cleaned["aired_from_year"].apply(
    lambda d: 1 if (d >= 1990) & (d < 2000) else 0)
anime_cleaned["00s"] = anime_cleaned["aired_from_year"].apply(
    lambda d: 1 if (d >= 2000) & (d < 2009) else 0)
anime_cleaned["10s"] = anime_cleaned["aired_from_year"].apply(lambda d: 1 if d >= 2010 else 0)

# Drop unnecessary features
anime_cleaned.drop(['title', 'title_english', 'title_japanese', 'title_synonyms', "background", "premiered", "broadcast", "related",
                    'image_url', 'status', 'aired', 'duration', 'type', 'source', 'airing',
                    'rating', "producer", "opening_theme", "ending_theme", "licensor", "aired_string",
                    "G - All Ages", "PG - Children", "PG-13 - Teens 13 or older", "R - 17+ (violence & profanity)",
                    "R+ - Mild Nudity", "Rx - Hentai", "None", "studio", "genre", "type_music", "aired_from_year"], axis=1, inplace=True)

# Separate tv and movie animes
anime_movies = anime_cleaned[(anime_cleaned["type_TV"] != 1) & (
    anime_cleaned["episodes"] == 1) & (anime_cleaned["duration_min"] > 40)]
anime_movies = anime_movies.drop(["episodes", "type_movie", "type_TV", "anime_id"], axis=1)

anime_series = anime_cleaned[(anime_cleaned["type_movie"] != 1) & (anime_cleaned["episodes"] > 1)]
anime_series = anime_series.drop(["type_movie", "type_TV", "anime_id"], axis=1)

anime_movies.to_csv("anime_movies.csv")
anime_series.to_csv("anime_series.csv")
