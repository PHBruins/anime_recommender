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


def getRecommendations(data,person,n=50,similarity=pearsonSimilarity):
    """
    Description: makes a dataframe with anime recommended for person
    :param data: the anime dataframe, person to which recommend anime for 
    and number of users person should be compared with
    :return: dataframe with recommended anime
    """
    
    #select the anime ranked by person
    prefs1 = data.loc[data['User'] == person].dropna(axis='columns').drop(['User'],axis=1)
    
    
    person_avg = 
    n_nearest_neighbors = topMatches(data,person)[0:n]
    ranking = n_nearest_neighbors['R_score']
    rating = n_nearest_neighbors['Avg_rating']
    
    #only keep the rating of users within to top n similarity ranking
    top =n_nearest_neighbors.merge(anime,on='User', how='left').drop(['User', 'R_score','Avg_rating'],axis=1).dropna(axis=1, how='all')
    
    
    #itterate over all anime which are ranked by similar user
    for column in top:
        Sums=0
        tot_rank=0
        tot=0
        #check if anime hasn't been seen by person 
        #and check whether there are enough ranking to be sure about recommendation
        #I chose treshold to be 5
        if column in prefs1 or top[column].count() < 6:
            continue
        #itterate over all rows and calculate similarity function for anime
        for i in top[column].iteritems():
            if pd.notna(i[1]):
                rank = ranking.iloc[i[0]]
                tot_rank =rank+tot_rank
                user_avg =rating.iloc[i[0]]
                sums = (i[1]-user_avg)*rank
                Sums = sums + Sums
                tot = person_avg + Sums/tot_rank
            #make sure anime are not ranked above 5 or below 0
            if tot >5:
                totals = pd.DataFrame({'anime': [column], 'recom': [5]})
            elif tot <0:
                totals = pd.DataFrame({'anime': [column], 'recom': [0]})
            else:
                totals = pd.DataFrame({'anime': [column], 'recom': [tot]})
            
        total= pd.concat([total,totals], ignore_index=True)

    total = total.sort_values(by = 'recom' ,ascending=False).reset_index(drop=True)

    return total
