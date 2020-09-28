import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



def user_user(input_beers, util_matrix):
    '''
    Recommends 10 beers by way of user-user collaborative filtering 


    inputs: lst - 5 beers on which to base recommendations
        
            DataFrame - beer to user utility matrix
    
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
    
    

    # sort by predicted ratings
    
    util_matrix = util_matrix.T.sort_values(27061, ascending=False).T
    

    # return top 10 after input beers 
    
    recommendations = list(util_matrix.columns[5:15])
    
    
    return recommendations







def user_user_existing(username, util_matrix):
    
    '''
    Recommends 10 beers to an existing user by way of user-user collaborative filtering


    inputs: str - user to make recommendations to
        
            DataFrame - beer to user utility matrix
    
    returns: lst - 10 beer recommendations

    '''
    
    
    # determine input beers (5 highest rated by username)
    
    input_beers = list(util_matrix.T.sort_values(username, ascending=False).T.columns)[:5]
    
    

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




def user_user_eval(username, reviews, util_matrix):
    
    '''
    Computes the average true percentile of recommended beers in a user's list of rated beers
    
    Inputs: str - Profile username for consumer of choice
    
            DataFrame - review log
    
            DataFrame - beer to user utility matrix
            
            
    
    Returns: float - user's average true rating percentile for 10 recommended beers
    
    '''
    
    # 10 recommended beers for user of interest
    
    recs = user_user_existing(username, util_matrix)
    
    
    # dataframe of user's ratings sorted descending
    
    user_df = reviews[reviews['review_profilename']==username].sort_values('review_overall')
    
    
    # list of beers rated by user in order of lowest to highest ratings
    
    beers_rated = list(user_df['beer_name'])
    
    
    # true percentiles accumulator
    
    percentiles = []
    
    
    # accumulate percentiles 
    
    for beer in recs:
        
        for i, rated in enumerate(beers_rated):
            
            if beer == rated:
                
                percentiles.append((i+1)/len(beers_rated))
        
        
    return (round(np.mean(percentiles), 3)) * 100



