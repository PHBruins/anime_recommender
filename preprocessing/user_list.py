import pandas as pd
from datetime import datetime
from datetime import date

# Load user_list dataset
user_list = pd.read_csv('./UserList.csv')

# Dummy gender
user_list = user_list[pd.notnull(user_list['gender'])]  # drops 84875 rows
dummy = pd.get_dummies(user_list['gender'])
user_list = pd.concat([user_list, dummy], axis=1)

# Drop unnecessary features
user_list = user_list.drop(['username', 'gender', 'location',
                            'access_rank', 'last_online', 'Non-Binary'], axis=1)

# Function to convert date to date stamp year


def convert(date_time):
    format = '%Y-%m-%d'  # The format
    year = pd.to_datetime(date_time, errors='coerce').year
    return year

# Function to calculate difference in today's year and given input


def calc(date_time):
    year = pd.to_datetime('today').year - date_time
    return year


# Applying convert function
user_list['join_date'] = user_list['join_date'].apply(convert)  # converts join date to join year

# Subtacting join date year from today's year
user_list['join_date'] = user_list['join_date'].apply(calc)

# Renaming join_date column
user_list = user_list.rename(columns={"join_date": "joined_years_ago"})

# Applying convert function
user_list['birth_date'] = user_list['birth_date'].apply(convert)  # converts join date to join year

# Subtacting birth date year from today's year
user_list['birth_date'] = user_list['birth_date'].apply(calc)

# Renaming birth_date column
user_list = user_list.rename(columns={"birth_date": "age"})

# Drop users with no age
user_list = user_list[pd.notnull(user_list['age'])]  # 56703 users

# Drop users that are less than 10 (must be error) or above 49 (don't watch anymore)
user_list = user_list[~(user_list['age'] < 10)]  # drops 564 users
user_list = user_list[~(user_list['age'] > 49)]  # drops 1281 users

# Creating dummy variables for age in following categories: less than 18, 18-25, 26-30 and 31+ years old
user_list['dummy_age_<18'] = user_list['age'].apply(lambda x: 1 if x < 18 else 0)  # 1139 users
user_list['dummy_age_18to25'] = user_list['age'].apply(
    lambda x: 1 if (x > 17) & (x < 26) else 0)  # 60558 users
user_list['dummy_age_26to30'] = user_list['age'].apply(
    lambda x: 1 if (x > 25) & (x < 31) else 0)  # 66064 users
user_list['dummy_age_31+'] = user_list['age'].apply(lambda x: 1 if (x > 30) else 0)  # 31491 users

# Drop age feature now that dummies have been created
user_list = user_list.drop(['age', "Male", "dummy_age_<18"], axis=1)

user_list.to_csv("user_list.csv")
