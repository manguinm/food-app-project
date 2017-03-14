
'''
Load data from recipe_ingredients_unique.csv into Relationship model
'''

# Full path and name to my csv file
data_path="/Users/Mel/foodappproject/database/recipe_ingredients_unique.csv"


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
from foodapp.models import Relationship

import csv
dataReader = csv.reader(open(data_path), delimiter=',', quotechar='"')

for row in dataReader:
	if row[0] != 'relationshipID': # Ignore the header row, import everything else
		relationship = Relationship()
		relationship.rel_id = row[0]
		relationship.ingredient_name = row[2]
		relationship.recipe_id = row[3]
		relationship.ingredient_id = row[4]
		relationship.save()
		