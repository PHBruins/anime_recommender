def topMatches(data, person):
    scores = []

    for i in data.itertuples():
        user = getattr(i, 'User')

        if user == person:
            continue

        person_data = data.loc[data['User'] == person].drop(['User'], axis=1)
        user_data = data.loc[data['User'] == user].drop(['User'], axis=1)
        user_avg = float(user_data.mean(axis=1))

        def pearsonSimilarity(person_data, user_data):
            """
            Description: function calculates pearson r
            :param data: the movie dataframe and the 2 persons to be compared
            :return: pearsons r similarity rating
            """

            def den(x, y):
                """
                Description: check if denomoninator is larger than 0
                :param data: scores from person1 and person 2
                :return:denominator
                """
                n = len(x)
                sum_x = np.sum(x)
                sum_y = np.sum(y)
                sum_x_sq = np.sum(x ** 2)
                sum_y_sq = np.sum(y ** 2)
                den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
                return den

            # check which anime are rated by both user and output this as a boolean array
            both_rated = np.array(np.logical_and(pd.notna(person_data), pd.notna(user_data))).flatten()

            # Use the boolean array produced before to slice the rows in order to only have anime ranked by both persons
            X = np.array(user_data.loc[:, both_rated]).flatten()
            Y = np.array(person_data.loc[:, both_rated]).flatten()

            # check if there are enough anime ranked by both person for pearsons r to have some meaning
            # I chose to set 5 as a minimum for users to be considered comparable
            if X.size < 6:
                r = float('nan')
            else:
                if den(X, Y) > 0:
                    # calculates pearsons r
                    r, sign = pearsonr(X, Y)
                else:
                    r = float('nan')

            return r

        similarity = pearsonSimilarity(person_data, user_data)

        if np.isnan(similarity):
            continue

        score = [[user, user_avg, similarity]]
        scores.extend(score)
    scores = pd.DataFrame(scores, columns=['User', 'Avg_rating', 'R_score'])
    scores = scores.sort_values(by='R_score', ascending=False).reset_index(drop=True)
    return scores
