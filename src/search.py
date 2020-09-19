import pandas as pd
import numpy as np


def beer_search(keyword, df):
    
    '''
    Returns a list of beers that contain a given keyword
    
    Inputs: str - keyword
    
            DataFrame: beers vs. ratings matrix
    
    Returns: lst - beers that match keyword
    
    '''
    
    beer_names = pd.Series(df['beer_name'].unique())
    
    boolean_array = beer_names.str.contains(keyword)
    
    indexes = []
    
    for i, flag in enumerate(boolean_array):
        if flag == True:
            indexes.append(i)
