import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



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




def content_eval(rating_df, sim_matrix, username):
    
    '''
    Computes difference between existing user's averaged actual ratings across top 10 
    recommended beers and their overall average rating given
    
    Inputs: DataFrame - All user ratings of beers
    
            DataFrame - Distance/similarity matrix of choice 
            
            str - Profile username for consumer of choice
    
    Returns: float - ratings residual
    
    '''
    
    # 10 recommended beers for user of interest
    
    recs = content_based_existing(username, sim_matrix, rating_df)
    
    # dataframe of user's ratings
    
    user_df = rating_df[rating_df['review_profilename']==username]
    
    # user's average ratings given
    
    avg_user_rating = np.mean(user_df['review_overall'])
    
    # true ratings for recommended beers
    
    ratings = []
    
    # append user's ratings for recommended beers if they exist
    
    for beer in recs:
        if beer in list(user_df['beer_name']):
            ratings.append(float(user_df[user_df['beer_name']==beer]['review_overall']))
    
    # difference between average true ratings across 10 recommended beers and average overall rating given 
    
    return round(np.mean(ratings) - avg_user_rating, 2)