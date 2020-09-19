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
