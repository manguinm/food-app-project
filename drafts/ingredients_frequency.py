'''
Set of functions for :
- measuring the frequency of ingredients among a set of recipes
- plot distributions
- removing noisy ingredients

'''

import seaborn as sns
import pandas as pd

def get_frequency_ingredients(df):
	'''
	Input : Dataframe where each column = 1 ingredient 
	n_rows = number of recipes
	n_columns = number of ingredients

	Output : Pandas Series with each ingredient_id and its frequency
	'''
	serie_freq = df.sum(axis=0)
	return serie_freq

def plot_dist_ingredients(df):

	serie_freq = get_frequency_ingredients(df)
	sns.set(color_codes=True)
	sns.distplot(serie_freq.values, kde=False, rug=True);

def n_most_frequent_ingredients(df, df_ingredients, n):
	# Returns list of n most frequent ingredients indices in a recipes dataframe
	# N.B. : the ingredients database needs to be provided in a dataframe format

	serie_freq = get_frequency_ingredients(df)
	idx_mostfreq_ing = serie_freq.order(ascending=False)[:n].index.astype(int).tolist()

	return idx_mostfreq_ing

def print_top_n_ingredients(df, df_ingredients, n):
	
	idx_top_n = n_most_frequent_ingredients(df, n, df_ingredients)	
	names_top_n = df_ingredients.ix[idx_top_n]['ingredients'].tolist()

	print ('The {0} most frequent ingredients are {1}'.format(n, names_top_n))


def n_least_frequent_ingredients(df, df_ingredients, n):
	# Returns list of n most frequent ingredients indices in a recipes dataframe
	# N.B. : the ingredients database needs to be provided in a dataframe format

	serie_freq = get_frequency_ingredients(df)
	idx_leastfreq_ing = serie_freq.order(ascending=True)[:n].index.astype(int).tolist()

	return idx_leastfreq_ing


def print_bottom_n_ingredients(df, df_ingredients, n):
	
	idx_bottom_n = n_least_frequent_ingredients(df, n, df_ingredients)	
	names_bottom_n = df_ingredients.ix[idx_bottom_n]['ingredients'].tolist()

	print ('The {0} least frequent ingredients are {1}'.format(n, names_bottom_n))	



def remove_n_top_ingredients(df, df_ingredients, n)	:
	'''
	Inputs :
	- n : number of top ingredients to remove (noisy ones)
	- df : dataframe of recipes
	- df_ingredients : dataframe of ingredients

	Output:
	- subset_df : subset of the recipes dataframe
	'''
	idx = n_most_frequent_ingredients(df, df_ingredients, n)
	str_idx = [str(item) for item in idx] # if the indices are 'str' in Pandas?
	subset_df = df.drop(str_idx, axis=1)

	return subset_df


