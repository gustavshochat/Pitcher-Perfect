import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def item_item(input_beers, reviews, sim_matrix, utility_matrix):
    
    '''
    Recommends 10 beers by way of item-item collaborative filtering

    inputs: lst - 5 input beers on which to base recommendations
            
            DataFrame - DataFrame - review log
            
            DataFrame - beer to beer similarity matrix
            
            DataFrame - beer to user utility matrix
    
    returns: lst - 10 beer recommendations

    '''
    
    
    # add row for new user to utility matrix
    
    utility_matrix.loc[len(utility_matrix)] = 0
     
    
    # create beer list and remove input beers
    
    beer_list = list(utility_matrix.columns)
    
    for beer in input_beers:
            beer_list.remove(beer)
            
    
    # fill in predicted ratings for user
    
    for beer in beer_list:
        
        # avg rating of beer
        
        avg_rating = reviews.groupby('beer_name').mean().loc[beer, 'review_overall']
        
        
        # sum of cosime similarity scores to input beers
        
        sim_score = np.sum(sim_matrix.loc[beer, input_beers])
        
        
        # avg ratings weighted by similarity score
        
        pred_rating = avg_rating * sim_score
        
        
        utility_matrix.loc[27061, beer] = pred_rating
    
    
    # sort by predicted ratings
    
    utility_matrix = utility_matrix.T.sort_values(27061, ascending=False).T
    
    
    # remove input beers
    
    utility_matrix = utility_matrix.drop(columns=input_beers)
    
    
    # beers with top 10 highest predicted ratings
    
    recommendations = list(utility_matrix.columns[:10])
    
    return recommendations





def item_item_existing(username, reviews, sim_matrix, utility_matrix):
    
    '''
    Recommends 10 beers to an existing user by way of item-item collaborative filtering
    
    
    inputs: str - name of user
    
            DataFrame - beer to beer similarity matrix
            
            DataFrame - review log
            
            DataFrame - beer to beer similarity matrix
            
            DataFrame - beer to user utility matrix
            
    '''
    
    
    # determine input beers (5 highest rated by username)
    
    input_beers = list(utility_matrix.T.sort_values(username, ascending=False).T.columns)[:5]
    
    
        # add row for new user to utility matrix
    
    utility_matrix.loc[len(utility_matrix)] = 0
     
    
    # create beer list and remove input beers
    
    beer_list = list(utility_matrix.columns)
    
    for beer in input_beers:
            beer_list.remove(beer)
            
    
    # fill in predicted ratings for user
    
    for beer in beer_list:
        
        # avg rating of beer
        
        avg_rating = reviews.groupby('beer_name').mean().loc[beer, 'review_overall']
        
        
        # sum of cosime similarity scores to input beers
        
        sim_score = np.sum(sim_matrix.loc[beer, input_beers])
        
        
        # avg ratings weighted by similarity score
        
        pred_rating = avg_rating * sim_score
        
        
        utility_matrix.loc[27061, beer] = pred_rating
    
    
    # sort by predicted ratings
    
    utility_matrix = utility_matrix.T.sort_values(27061, ascending=False).T
    
    
    # remove input beers
    
    utility_matrix = utility_matrix.drop(columns=input_beers)
    
    
    # beers with top 10 highest predicted ratings
    
    recommendations = list(utility_matrix.columns[:10])
    
    return recommendations





def item_item_eval(username, reviews, utility_matrix, sim_matrix):
    
    '''
    Computes the average true percentile of recommended beers in a user's list of rated beers
    
    Inputs: str - Profile username for consumer of choice
            
            DataFrame - review log
    
            DataFrame - beer to user utility matrix
            
            DataFrame - beer to beer similarity matrix
            
    
    Returns: float - user's average true rating percentile for 10 recommended beers
    
    '''
    
    # 10 recommended beers for user of interest
    
    recs = item_item_existing(username, reviews, sim_matrix, utility_matrix)
    
    
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


