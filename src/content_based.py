import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity



def content_based(beer_list, sim_matrix):
    
    '''
    recommends 10 beers based on 5 input beers of choice
    
    Inputs: lst - 5 beers to base recommendations on
            DataFrame - beer similarity matrx
            
            
    Returns: list - 10 beer names
            
    '''
                
    candidates = []
                
    for beer in beer_list:
        
        # dataframe with 10 rows (most similar beers), two columns (name, similarity)       
                
        similar_df = sim_matrix[beer].nlargest(11).reset_index().iloc[1:]
        
        # append beer name/similarity tuples to candidates list
                
        for i in range(10):
            candidates.append((similar_df.iloc[i, 0], similar_df.iloc[i, 1]))
    
    # sort candidates list by highest similarity
    
    candidates = sorted(candidates, key = lambda x: x[1], reverse=True)
    
    # instantiate set of recommendations 
    
    recommendations = set()
    
    # recommend beers with 10 highest similarity score to 5 original beers w/o repeats 
                
    for beer in candidates:    
        
        if beer[0] in beer_list:
            continue
            
        if len(recommendations) == 10:
            break 
            
        else:
            recommendations.add(beer[0])
    
    return recommendations





def content_based_existing(user_name, sim_matrix, rating_df):
    
    '''
    Recommends 10 beers to an existing user based on item to item similarity
    

    Inputs: str - customer profile name
            dataframe - distance matrx
            dataframe - all ratings for top 1000 most rated beers
            
    Returns: list - 10 beer names
            
    '''
    
    # dataframe of ratings by user of interest           
                
    user_df = rating_df[rating_df['review_profilename']==user_name].sort_values(by='review_overall', ascending=False)
    
    # top 5 highest rated beers by user            
                
    top_5_beers = list(user_df.iloc[:5]['beer_name'])

    # candidates accumulator          
                
    candidates = []
                
    for beer in top_5_beers:
        
        # dataframe with 10 rows (most similar beers), two columns (name, similarity)       
                
        similar_df = sim_matrix[beer].nlargest(11).reset_index().iloc[1:]
        
        # append beer name/similarity tuples to candidates list
                
        for i in range(10):
            candidates.append((similar_df.iloc[i, 0], similar_df.iloc[i, 1]))
    
    # sort candidates list by highest similarity
    
    candidates = sorted(candidates, key = lambda x: x[1], reverse=True)
    
    # instantiate set of recommendations 
    
    recommendations = set()
    
    # recommend beers with 10 highest similarity score to 5 original beers w/o repeats 
                
    for beer in candidates:
        if len(recommendations) == 10:
            break 
        else:
            recommendations.add(beer[0])
    
    return recommendations





def content_based2(beer_list, sim_matrix):
        
    '''
    recommends 10 beers based on 5 input beers of choice
    
    Inputs: lst - 5 beers to base recommendations on
            DataFrame - beer similarity matrx
            
            
    Returns: list - 10 beer names
            
    '''
                
    candidates = []
                
    for beer in beer_list:
        
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





def content_based_existing2(user_name, sim_matrix, rating_df):
        
    '''
    Recommends 10 beers to an existing user based on item to item similarity
    

    Inputs: str - customer profile name
            dataframe - distance matrx
            dataframe - all ratings for top 1000 most rated beers
            
    Returns: list - 10 beer names
            
    '''
    
    # dataframe of ratings by user of interest           
                
    user_df = rating_df[rating_df['review_profilename']==user_name].sort_values(by='review_overall', ascending=False)
    
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








def content2_eval(rating_df, sim_matrix, username):
    
    '''
    Computes difference between existing user's averaged actual ratings across top 10 
    recommended beers and their overall average rating given
    
    Inputs: DataFrame - All user ratings of beers
    
            DataFrame - Distance/similarity matrix of choice 
            
            str - Profile username for consumer of choice
    
    Returns: float - ratings residual
    
    '''
    
    # 10 recommended beers for user of interest
    
    recs = content_based_existing2(username, sim_matrix, rating_df)
    
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