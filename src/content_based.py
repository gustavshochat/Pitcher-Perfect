import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def content_based(input_beers, sim_matrix):
        
    '''
    recommends 10 beers based on similarity to 5 input beers

    Inputs: lst - 5 beers to base recommendations on
            DataFrame - beer to beer similarity matrix
            
            
    Returns: list - 10 beer names
            
    '''
                
    candidates = []
                
    for beer in input_beers:
        
        # dataframe with 10 rows (most similar beers), two columns (name, similarity)       
                
        similar_df = sim_matrix[beer].nlargest(11).reset_index().iloc[1:]
        
        
        # add two most similar beers that are not already candidates for recommendation
                
        count = 0
    
        for i in range(10):
            
            name = similar_df.iloc[i, 0]
            
            if name in candidates or name in input_beers:           
                continue
                
            if count == 2:
                break
            
            else:
                candidates.append(name)
                count += 1
    
    return candidates





def content_based_existing(username, reviews, sim_matrix):
        
    '''
    Recommends 10 beers to an existing user based on similarity to their top 5
               most highly rated beers
    

    Inputs: str - user profile name
            dataframe - review log
            dataframe - beer to beer similarity matrix
            
            
    Returns: list - 10 beer names
            
    '''
    
    # dataframe of ratings by user of interest           
                
    user_df = reviews[reviews['review_profilename']==username].sort_values(by='review_overall', ascending=False)
    
    # top 5 highest rated beers by user            
                
    top_5_beers = list(user_df.iloc[:5]['beer_name'])

    # candidates accumulator          
                
    candidates = []
                
    for beer in top_5_beers:
        
        # dataframe with 10 rows (most similar beers), two columns (name, similarity)       
                
        similar_df = sim_matrix[beer].nlargest(11).reset_index().iloc[1:]
        
        
        # add two most similar beers that are not already candidates for recommendation
                
        count = 0
    
        for i in range(10):
            
            name = similar_df.iloc[i, 0]
            
            if name in candidates:           
                continue
                
            if count == 2:
                break
            
            else:
                candidates.append(name)
                count += 1
    
    return candidates




def content_based_eval(username, reviews, sim_matrix):
    
    '''
    Computes the average true percentile of recommended beers in a user's list of rated beers
    
    Inputs: DataFrame - All user ratings of beers
    
            DataFrame - Distance/similarity matrix of choice 
            
            str - Profile username for consumer of choice
    
    Returns: float - user's average true rating percentile for 10 recommended beers
    
    '''
    
    # 10 recommended beers for user of interest
    
    recs = content_based_existing(username, reviews, sim_matrix)
    
    
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
        
        
    return round(np.mean(percentiles), 3) * 100




