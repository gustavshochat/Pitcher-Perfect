import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



def collab_filter(input_beers, util_matrix):
    '''
    Recommends 10 beers based on user to user similarity 


    inputs: lst - 5 beers on which to base recommendations
        
            DataFrame - utility matrix of users and beers
    
    returns: lst - 10 beer recommendations

    '''

    # add row for new user to utility matrix
    
    util_matrix.loc[len(util_matrix)] = 0
    
    
    # populate ratings of input beers for new user
    
    util_matrix.iloc[len(util_matrix) - 1][input_beers] = 5
    
    
    # create beer list and remove input beers
    
    beer_list = list(util_matrix.columns)
    
    for beer in input_beers:
            beer_list.remove(beer)
     
    
    # list of users         
            
    users = list((util_matrix.index))
    
    
    # cosine similarities between new user and existing users
    
    cosims = np.array([ (cosine_similarity([util_matrix.iloc[-1][input_beers]], [util_matrix.loc[user][input_beers]]))[0][0] for user in users])
    
    
    # add cosims as a column and change new user's to -100
    
    util_matrix['cosim'] = cosims
    
    util_matrix.loc[27061, 'cosim'] = -100
    
    
    # sort user rows by cosine similarity

    util_matrix = util_matrix.sort_values(by=['cosim'], ascending=False)
    
    
    # fill in predicted ratings for user
    
    for beer in beer_list:
    
        # dataframe of 10 most similar users that have rated beer 
    
        df = util_matrix[util_matrix[beer]!=0].iloc[:10]
    
    
        # assign rating to average of weighted reviews
    
        df['weighted_rating'] = df[beer] * df['cosim']
    
    
        # assign rating to averaged weighted rating
    
        rating = np.mean(df['weighted_rating'])
    
    
        # fill in predicted ratings for new user
    
        util_matrix.loc[27061, beer] = rating
    
    
    
    util_matrix = util_matrix.T.sort_values(27061, ascending=False).T
    
    
    recommendations = list(util_matrix.columns[5:15])
    
    
    return recommendations







def collab_filter_existing(user, util_matrix):
    
    '''
    Recommends 10 beers to an existing user via collaborative filtering


    inputs: str - username to make recommendations to
        
            DataFrame - utility matrix of users and beers
    
    returns: lst - 10 beer recommendations

    '''
    
    
    # determine input beers (5 highest rated by username)
    
    input_beers = list(util_matrix.T.sort_values(user, ascending=False).T.columns)[:5]
    
    

    # add row for new user to utility matrix
    
    util_matrix.loc[len(util_matrix)] = 0
    
    
    # populate ratings of input beers for new user
    
    util_matrix.iloc[len(util_matrix) - 1][input_beers] = 5
    
    
    # create beer list and remove input beers
    
    beer_list = list(util_matrix.columns)
    
    for beer in input_beers:
            beer_list.remove(beer)
     
    
    # list of users         
            
    users = list((util_matrix.index))
    
    
    # cosine similarities between new user and existing users
    
    cosims = np.array([ (cosine_similarity([util_matrix.iloc[-1][input_beers]], [util_matrix.loc[user][input_beers]]))[0][0] for user in users])
    
    
    # add cosims as a column and change new user's to -100
    
    util_matrix['cosim'] = cosims
    
    util_matrix.loc[27061, 'cosim'] = -100
    
    
    # sort user rows by cosine similarity

    util_matrix = util_matrix.sort_values(by=['cosim'], ascending=False)
    
    
    # fill in predicted ratings for user
    
    for beer in beer_list:
    
        # dataframe of 10 most similar users that have rated beer 
    
        df = util_matrix[util_matrix[beer]!=0].iloc[:10]
    
    
        # assign rating to average of weighted reviews
    
        df['weighted_rating'] = df[beer] * df['cosim']
    
    
        # assign rating to averaged weighted rating
    
        rating = np.mean(df['weighted_rating'])
    
    
        # fill in predicted ratings for new user
    
        util_matrix.loc[27061, beer] = rating
    
    
    # sort on predicted ratings
    
    util_matrix = util_matrix.T.sort_values(27061, ascending=False).T
    
    
    # recommend top 10 (skipping top 5 input beers)
    
    recommendations = list(util_matrix.columns[5:15])
    
    
    return recommendations





def collab_eval(rating_df, util_matrix, username):
        
    '''
    Computes the average difference between a user's true ratings for
    10 recommended beers and their average rating across all beers
    
    inputs: DataFrame - user ratings of beers
    
            DataFrame - beer/user utility matrix
            
            str - name of existing user

    '''
    
    
    # generate recommendations for existing user
    
    recs = collab_filter_existing(username, util_matrix)
    
    
    # create dataframe of user's ratings
    
    user_df = rating_df[rating_df['review_profilename']==username]
    
    
    # compute average rating given by user
    
    avg_user_rating = np.mean(user_df['review_overall'])
    
    
    # accumulate true ratings of recommended beers
    
    ratings = []
    
    for beer in recs:
        if beer in list(user_df['beer_name']):
            ratings.append(float(user_df[user_df['beer_name']==beer]['review_overall']))
    

    # return average residual between true rating and average rating

    return round(np.mean(ratings) - (avg_user_rating), 2)