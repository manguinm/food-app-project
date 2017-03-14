
'''
Load data from recipe_final_utf8.csv into Recipe model
and correspondances to ingredients are added from 'q.csv'
'''

# Full path and name to my csv file
recipedata_path="/Users/Mel/foodappproject/database/recipe_final_clean.csv"
correspondances_path = "/Users/Mel/foodappproject/database/q.csv"


import os, sys

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
from foodapp.models import Relationship, Recipe

import csv

dataReader = csv.reader(open(recipedata_path), delimiter=',', quotechar='"')
corrReader = csv.reader(open(correspondances_path), delimiter=',', quotechar='"')

with open(correspondances_path, 'r') as f:
    correspondances_data = [row for row in csv.reader(f.read().splitlines())][1:] # ignore header row 

with open(recipedata_path, 'r') as f:
    recipes_data = [row for row in csv.reader(f.read().splitlines())][1:] # ignore header row 

for i, row in enumerate(recipes_data):
	#if row[0] != 'id': # Ignore the header row, import everything else
	recipe = Recipe()
	recipe.rid = int(row[3])
	recipe.recipe_name = row[1]
	recipe.number_steps = int(row[2])
	#recipe.instructions = row[4]
		


# Add for each recipe the vector of 0s or 1s of length n_ingredients that indicates which ingredient is needed
# for this recipe (col i =1 if ingredient i is needed, 0 otherwise)


	corresponding_row = correspondances_data[i]
	#ing= corresponding_row[1:] # take the whole line except the index
	ing = list(map(int, corresponding_row[1:]))
	recipe.ingredients = ing
	recipe.save()
'''
		# Add the Many-to-Many Relationship with ingredient_id
		ingredients_recipe = Relationship.objects.filter(recipe_id =row[5]).values_list('ingredient_id', flat=True)
		for ingredient in ingredients_recipe:
			recipe.ingredient_id.add(ingredient)
		recipe.save()
'''	





		