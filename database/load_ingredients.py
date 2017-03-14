
# Full path and name to my csv file
data_ingredients_path="/Users/Mel/foodappproject/database/top131ingredients.csv"


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
from foodapp.models import Ingredient

import csv
dataReader = csv.reader(open(data_ingredients_path), delimiter=',', quotechar='"')

for row in dataReader:
	if row[0] != 'ingredients': # Ignore the header row, import everything else
		ingredient = Ingredient()
		ingredient.iid = row[12]
		ingredient.ingredient_name = row[0]
		ingredient.serving_size = row[2]
		ingredient.unit = row[3]
		ingredient.package_size = row[4]
		ingredient.price = row[5]
		ingredient.calories = row[6]
		ingredient.fat = row[7]
		ingredient.fiber = row[8]
		ingredient.sugar = row[9]
		ingredient.protein = row[10]
		ingredient.save()