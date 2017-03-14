'''
ILP Formulation for PuLP Modeller

How to import django models in python scripts : (or simply just do as for the load_data.py file !)
http://stackoverflow.com/questions/19475955/using-django-models-in-external-python-script
'''
# Full path and name to any csv files I need
# data_ingredients_path="/Users/Mel/foodappproject/database/top131ingredients.csv"


import os, sys
import itertools
import string

proj_path = "/Users/Mel/foodappproject/"

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# import your modules and use them just like you do in your web apps
from foodapp.models import Ingredient, Recipe, Relationship

# Import PuLP modeler functions
from pulp import *

# Import data from Django databases as dictionaries


# Indices
tmp_ing = Ingredient.objects.values_list('iid').order_by('iid')
tmp_recipes = Recipe.objects.values_list('rid').order_by('rid')
idx_ingredients = list(itertools.chain(*tmp_ing))
idx_recipes = list(itertools.chain(*tmp_recipes))


# Parameters for ingredients : 
dict_weights = dict(Ingredient.objects.values_list('iid', 'user_preference'))
dict_costs = dict(Ingredient.objects.values_list('iid', 'price'))
dict_pkgsize = dict(Ingredient.objects.values_list('iid', 'package_size'))
dict_calories = dict(Ingredient.objects.values_list('iid', 'calories'))
dict_fat = dict(Ingredient.objects.values_list('iid', 'fat'))
dict_fiber = dict(Ingredient.objects.values_list('iid', 'fiber'))
dict_sugar = dict(Ingredient.objects.values_list('iid', 'sugar'))
dict_protein = dict(Ingredient.objects.values_list('iid', 'protein'))

# Convert these dicts' values to int :

dict_weights_ints = dict((k,float(v)) for k,v in dict_weights.items())
dict_costs_ints = dict((k,float(v)) for k,v in dict_costs.items())
dict_pkgsize_ints = dict((k,int(v)) for k,v in dict_pkgsize.items())
dict_pkgsize_ints = dict((k,int(v)) for k,v in dict_pkgsize.items())
dict_calories_ints = dict((k,int(v)) for k,v in dict_calories.items())
dict_fat_ints = dict((k,int(v)) for k,v in dict_calories.items())





# Parameters for recipes
dict_nbofsteps = dict(Recipe.objects.values_list('rid', 'number_steps'))


'''
Parameters for both recipes and ingredients
- SEEMS NOT TO BE ANY INFO ON qij : amount of ingredient j needed for recipe i 
- take qij = 1 if ingredient j needed for recipe i, 0 otherwise 
'''
 

#def clean_str_int(vect):
#    '''
#    Cleans the string vector and returns a list of int.
#    Input :
#    - String object of type "['1', '0', ...,]
#    
#    Output :
#    - List of ints : [1,0,...,]
#    '''
#    list_int = []
#    splitted = vect.split()
#    for item in splitted:
#        #cleanstring = string.translate(None, "[]'',")
#        #cleanstring = string.translate(string.maketrans("[]'',", ""))
#        cleanitem = item.translate({ord(i):None for i in "[],''"})
#        integer=int(cleanitem)
#        list_int.append(integer)
#    return list_int 


list_rec_ing = list(Recipe.objects.values_list('rid', 'ingredients')) # list of tuples ('rid', 'ingredients')
dict_correspondances = {}

for elem in  list_rec_ing:
	rid = elem[0]
	ing_vector = elem[1]
	for idx, value in enumerate(ing_vector):
		dict_correspondances[rid, idx + 1] = value # fill a dictionary where key is (rid,iid) and value is 1 or 0 depending on if ingredient j is needed for recipe i


#print(dict_correspondances)
    
# Create the 'prob' variable to contain the problem data
prob = LpProblem("Recipes Recommendation", LpMaximize)        

# Create variables

# Recipe_var = 1 if recipe i is chosen, 0 otherwise
recipe_vars = LpVariable.dicts("Recipe", idx_recipes, 0, 1, LpBinary)

# ingredient_var = 1 if ingredient j is chosen, 0 otherwise
ingredient_vars = LpVariable.dicts("Ingredient", idx_ingredients, 0, 1, LpBinary)

# nb of packages of ingredient j to buy
package_vars = LpVariable.dicts("Package", idx_ingredients, 0, 100, LpInteger)

# Parameters
# upper bound for nutrients (calories, fat, fiber, sugar, protein)
nutr_max = [18000,5500,200,11000,6000];
cal_max = 18000;
fat_max = 5500;
fiber_max=200;
sugar_max=11000;
protein_max=6000;

# lower bound for nutrients
nutr_min=[14000,1000,20,1000,500];
cal_min = 0; # or infeasible pb
fat_min = 14000;
fiber_min=20;
sugar_min=1000;
protein_min=500;

#upper bound for number of steps
t_max = 75;

#upper bound for cost
c_max = 45;

#upper bound for number of meals
meals_max = 16;

#lower bound for number of meals
meals_min = 10;



# Objective function added to the prob variable first
prob += lpSum(ingredient_vars[j]*dict_weights[j] for j in idx_ingredients), "Maximize user preferences for ingredients"

# Adding constraints :

prob += lpSum(package_vars[j]*dict_costs[j] for j in idx_ingredients) <= c_max # "Budget constraint"
prob += lpSum(recipe_vars[i]*dict_nbofsteps[i] for i in idx_recipes) <= t_max #, "Time constraint"


for j in idx_ingredients:
    for i in idx_recipes:
        prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_calories[j] <= cal_max #, "Calories max"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_calories[j] >= cal_min #, "Calories min"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_fat[j] <= fat_max #, "Fat max"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_fat[j] >= fat_min#, "Fat min"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_fiber[j] <= fiber_max#, "Fiber max"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_fiber[j] >= fiber_min#, "Fiber min"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_sugar[j] <= sugar_max#, "Sugar max"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_sugar[j] >= sugar_min#, "Sugar min"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_sugar[j] <= protein_max#, "Protein max"
        #prob += recipe_vars[i]*dict_correspondances[(i,j)]*dict_sugar[j] >= protein_min#, "Protein min"
        #prob+= lpSum(recipe_vars[i]*dict_correspondances[(i,j)] for i in idx_recipes) <= package_vars[j]*dict_pkgsize[j] 
        #, quantity constraint
      
prob += lpSum(recipe_vars[i] for i in idx_recipes) <= meals_max#, "Number of meals upper bound"  
prob += lpSum(recipe_vars[i] for i in idx_recipes) >= meals_min#, "Number of meals lower bound"

prob.solve()

 # The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

'''
random_recipes_list = Recipe.objects.all().order_by('?')[:10]
print("According to your tastes, here is a recommended lit of recipes:", random_recipes_list)

#print Ingredient.objects.values_list('iid').order_by('user_preference')[:10]

def print_result(recipe_list, )
'''

# Print the chosen recipes

