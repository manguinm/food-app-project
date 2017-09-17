'''
Set of functions relative to Jaccard measure of similarity (relevant for binary vectors)

'''
import numpy as np
from sklearn.metrics import jaccard_similarity_score
import pandas as pd

def jaccard_matrix(array):
    '''
    Input : array of binary vectors
    Output : Square matrix (array) of Jaccard coefficients
    '''
    
    list_jscore = []
    for row in array:
        row_jscore = []
        for otherrow in array:
            j_score = jaccard_similarity_score(row, otherrow)
            row_jacsim.append(jaccoef)
        list_jscore.append(row_jacsim)
        array_jscore = np.array(list_jscore)
        
    return array_jscore

def save_jaccard_matrix(array,filepath): 
	np.savetxt(filepath, array, delimiter=',')   

 
 def get_top_n_similar(n, recipe_id, df, 1st_jacc_column):
    '''
    Given the recipe_id number and the desired number n of most similar recipes, returns a list of most similar
    recipes in descending order from a dataframe.
    NB : the 1st most similar one should be the recipe itself.
    NB 2 : Need to give the 1st column number of jaccard coefficients. 
    
    '''
    this_recipe = df.loc[recipe_id]
    list_jaccoefs = this_recipe.iloc[1st_jacc_column:].tolist()
    
    # Sorting the Jaccard coefficients of all other recipes with this one by descending order
    from operator import itemgetter
    indices, list_jaccoefs_sorted = zip(*sorted(enumerate(list_jaccoefs), key=itemgetter(1), reverse=True))
    
    # Taking the first n recipes
    list_recipes = df['title'].tolist()
    top_n = indices[:n]
    top_n_similar_this_recipe = [list_recipes[i] for i in top_n]
    
    return top_n_similar_this_recipe  

def get_top_n_dissimilar(n, recipe_id, df, 1st_jacc_column):
    '''
    Given the recipe_id number and the desired number of most similar recipes, returns a list of least similar
    recipes in ascending order. (the worst the first)
    NB 2 : Need to give the 1st column number of jaccard coefficients. 
    '''
    this_recipe = df.loc[recipe_id]
    list_jaccoefs = this_recipe.iloc[5:].tolist()
    
    # Sorting the Jaccard coefficients of all other recipes with this one by ascending order
    from operator import itemgetter
    indices, list_jaccoefs_sorted = zip(*sorted(enumerate(list_jaccoefs), key=itemgetter(1)))
    
    # Taking the first n recipes
    list_recipes = df['title'].tolist()
    top_n = indices[:n]
    top_n_dissimilar_this_recipe = [list_recipes[i] for i in top_n]
    
    return top_n_dissimilar_this_recipe         
