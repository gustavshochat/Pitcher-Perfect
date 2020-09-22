import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF


def factorize_users(util_matrix, x):
    
    '''
    Generates user to feature similarity matrix
    
    
    inputs: DataFrame - beer to user utility matrix
    
            int - number of latent features to compress data into
            
    
    returns: DataFrame -  user to feature similarity matrix
    
    '''
    
    # instantiate factorization
    
    model = NMF(n_components=x, init='random', random_state=0)
    
    
    # factorized matrices
    
    W = model.fit_transform(util_matrix)
    
    H = model.components_
    
    
    # renaming columns to match user labels
    
    user_names= list(util_matrix.T.columns)
    
    d_users = {}
    
    
    for i in range(len(user_names)):
        d_users[i] = user_names[i]   
    
    user_matrix = pd.DataFrame(W).T.rename(columns=d_users).T  
    
    return user_matrix






def factorize_beers(util_matrix, x):
    
    '''
    Generates beer to feature similarity matrix
    
    
    inputs: DataFrame - beer to user utility matrix
    
            int - number of latent features to compress data into
            
    
    returns: DataFrame - beer to feature similarity matrix 
    
    '''
        
    # instantiate factorization
    
    model = NMF(n_components=x, init='random', random_state=0)
    
    
    # factorized matrices
    
    W = model.fit_transform(util_matrix)
    
    H = model.components_
    
    
    # renaming columns to match beer labels
    
    beer_names = list(util_matrix.columns)
                      
    d_beers = {}                 

    for i in range(len(beer_names)):
        d_beers[i] = beer_names[i]    
    
    
    beer_matrix = pd.DataFrame(H).rename(columns=d_beers).T
                      
    return beer_matrix




def nmf_beer_sim(beer_to_feature):
    
    '''
    Generates a cosine similairty matrix of beers based on latent features
    
    inputs: DataFrame - beer to latent feature similarity matrix, H in NMF
    
    returns: DataFrame - cosim matrix
    
    
    '''
    
    
    # create cosine similarity matrix
    
    cosine_nmf = pd.DataFrame(cosine_similarity(beer_to_feature))
    
    
    # rename rows/columns to match beer labels
    
    beer_names = list(beer_to_feature.T.columns)

    d_beers = {}                 

    for i in range(len(beer_names)):
        d_beers[i] = beer_names[i] 
    
    cosine_nmf = cosine_nmf.rename(columns = d_beers).T.rename(columns = d_beers)
    
    return cosine_nmf





def nmf_user_sim(user_to_feature):
    
    '''
    Generates a cosine similairty matrix of users based on latent features
    
    inputs: DataFrame - beer to latent feature similarity matrix, H in NMF
    
    returns: DataFrame - cosim matrix
    
    
    '''
    
    # create similarity matrix
    
    user_names = list(user_to_feature.T.columns)
    
    
    # rename rows/columns to match user labels
    
    d_users = {}
    
    for i in range(len(user_names)):
        d_users[i] = user_names[i]
        
    users_sim = pd.DataFrame(cosine_similarity(user_to_feature))
    
    users_sim = users_nmf.rename(d_users)
    
    users_sim = users_sim.rename(columns=d_users)
    
    return users_sim





def content_nmf(beer_list, sim_matrix):
    
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
            
            if count == 2:
                break
            
            if name not in candidates and name not in beer_list:           
                candidates.append(name)
                count += 1
                
    return candidates







def content_nmf_existing(user_name, sim_matrix, rating_df):
    
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
                
    beer_list = list(user_df.iloc[:5]['beer_name'])

    # candidates accumulator          
                
    candidates = []
                
    for beer in beer_list:
        
        # dataframe with 10 rows (most similar beers), two columns (name, similarity)       
                
        similar_df = sim_matrix[beer].nlargest(11).reset_index().iloc[1:]
        
        
        # add two most similar beers that are not already candidates for recommendation
                
        count = 0
        
    
        for i in range(10):
            
            name = similar_df.iloc[i, 0]
            
            if count == 2:
                break
            
            if name not in candidates and name not in beer_list:           
                candidates.append(name)
                count += 1
                
    return candidates





def content_nmf_eval(rating_df, sim_matrix, username):
    
    '''
    Computes difference between existing user's averaged actual ratings across top 10 
    recommended beers and their overall average rating given
    
    Inputs: DataFrame - All user ratings of beers
    
            DataFrame - Distance/similarity matrix of choice 
            
            str - Profile username for consumer of choice
    
    Returns: float - ratings residual
    
    '''
    
    # 10 recommended beers for user of interest
    
    recs = nmf_content_existing(username, sim_matrix, rating_df)
    
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






def latent_styles(df, util_matrix, x):
    
    '''
    Reveals the top 5 beer styles for each latent feature of a factorized utility matrix
    
    
    inputs: DataFrame - utility matrix of beers and consumers
    
            int - number of latent features to extract
    
    returns: dict - latent features keys mapping to beer styles
    '''
    
    # instantiate NMF
    
    model = NMF(n_components=x, init='random', random_state=0)
    
    
    
    # factorized matrices
    
    W = model.fit_transform(util_matrix)
    H = model.components_
    
   

    # names of beers
    
    beer_names = list(util_matrix.columns)
    
    
    
    # feature to item similarity matrix with beer names added
    
    nmf_matrix = pd.DataFrame(H)
    
    d = {}

    for i in range(len(beer_names)):
        d[i] = beer_names[i]
        
    nmf_matrix = nmf_matrix.rename(columns=d).T
    
    
    # feature to beer dictionary
    
    latent_beer = {}

    for i in range(x):
        latent_beer[i] = []
    
    for beer in beer_names:
    
        latent_beer[np.argmax(nmf_matrix.loc[beer])] += [beer]
        
    
    # beer to style dictionary
    
    beer_style = {}

    for beer in beer_names:
    
        beer_style[beer] = df[df['beer_name']==beer].iloc[0, :]['beer_style']
        
    
    
    # feature to style dictionary
    
    latent_style = {}
    
    for i in range(x):
        latent_style[i] = []
        
    for i, feat in enumerate(list(latent_beer.values())):
        for beer in feat:
            latent_style[i] += [beer_style[beer]]
    
    
    
    # function to return feature to top 5 style dictionary
    
    def style_counter(latent_style):

        result = {}
    
        for k, v in latent_style.items():
            d = {}
        
            for style in v:            
                if style in d:               
                    d[style] +=1                   
                else:               
                    d[style] = 1
        
            lst = []
        
            for idx in np.argsort(list(d.values())[-5:]):           
                lst.append(list(d.keys())[idx])
                                                
            result[k] = lst       
    
        return result   
    
    return style_counter(latent_style)