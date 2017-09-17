
# Food App Project

## Web app for recommendation of recipes & groceries lists based on learning users' food tastes.


### Contributors : Melanie Manguin

This repository provides the source code for a web app that recommends the user a list of recipes and a grocery list, with number of packages per ingredient, by learning a user's preferences. The recipes (~15k) were scraped from open-source cooking websites.

### Tools used:
Built in Django, using PuLP for integer-linear programming, PostgreSQL as the database.

Research around recipes similarities can be found in the folder `drafts`, in Jupyter notebooks format. 

### Requirements:
* Python 3.6

* Set up a virtual environment : `python3 -m venv myvenv`

* last version of Django (1.11 or later)
  * first, upgrade pip : `(myvenv) ~$ pip install --upgrade pip`
  * second, install Django using pip : `(myvenv) ~$ pip install django~=1.11.0`


### Getting started

* Download the repo
* In the current project directory, start the server by typing in the command line: `python manage.py runserver`
* Access the web app home page at the follozing URL: `http://127.0.0.1:8000/foodapp/`
