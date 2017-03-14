from django.db import models

# Create your models here.

from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.postgres.fields import ArrayField


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Ingredient(models.Model):
	iid = models.IntegerField(unique=True) # Need to specify the id as Django creates it automatically right ?
	ingredient_name = models.CharField(max_length=200, unique=True)
	# recipe_id = models.ManyToManyField(Recipe, symmetrical = True) # DO IT LATER
	user_preference = models.FloatField(default=0)
	serving_size = models.FloatField(default=0)
	unit = models.CharField(max_length=200, default=0)
	package_size = models.FloatField(default=0) 
	price = models.FloatField(default=0)
	calories =  models.FloatField(default=0)
	fat = models.FloatField(default=0)
	fiber = models.FloatField(default=0)
	sugar = models.FloatField(default=0)
	protein = models.FloatField(default=0)

	def __str__(self):
		return self.ingredient_name


class Relationship(models.Model):
	rel_id = models.IntegerField(unique=True)
	ingredient_name = models.CharField(max_length=200)
	recipe_id = models.IntegerField(default=0)
	ingredient_id = models.IntegerField(default=0)

	def __str__(self):
		#return "Recipe-ingredient pair: recipe '{0}', ingredient '{1}'".format(self.recipe_id, self.ingredient_id)
		return  "Recipe-ingredient pair: recipe %d, ingredient %d " % (self.recipe_id, self.ingredient_id)

class Recipe(models.Model):
	rid = models.IntegerField(unique=True)
	#ingredient_id = models.ManyToManyField(Relationship, symmetrical = True) # END UP WITH AN INTEGRITY ERROR 
	recipe_name = models.CharField(max_length=200, unique=True)
	number_steps = models.IntegerField(default=0)
	instructions = models.TextField()
	ingredients = ArrayField((models.IntegerField()))
	ranking = models.FloatField(default=5)



	def __str__(self):
		return self.recipe_name		

