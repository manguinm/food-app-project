from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Ingredient, Recipe, Relationship
from django.urls import reverse
from django.db import IntegrityError, transaction
from foodapp.forms import RankRecipeForm, BaseRankRecipeFormSet
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from django.contrib import messages

import os
from mysite.settings import BASE_DIR
pulp_path = os.path.join(BASE_DIR, 'pulp/')


# Create your views here.

def index(request):
	ingredient_list= Ingredient.objects.order_by('iid')[:20] # display on 10 first ingredients
	context = {'ingredient_list': ingredient_list}
	return render(request, 'foodapp/index.html', context)

def ingredient_detail(request, ingredient_id):
	ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
	return render(request, 'foodapp/ingredient-detail.html', {'ingredient': ingredient})

def preferences_ingredient(request, ingredient_id):
	ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
	return render(request, 'foodapp/preferences-ingredient.html', {'ingredient': ingredient})  


def rank_ingredient(request, ingredient_id):
	#return HttpResponse("You're ranking ingredient %s." % ingredient_id)
	
	ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
	try:
		new_preference = request.POST['preference']
		ingredient.user_preference = new_preference


	    # TO BE CHANGED !
	except (KeyError, Ingredient.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'foodapp/ingredient.html', {
			'ingredient': ingredient,
			'error_message': "You didn't set up a value for your preferences.",
		})
	else:
		ingredient.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('foodapp:ingredient_detail', args=(ingredient.iid,)))

def run_model(request):
	return render(request, 'foodapp/run-model.html', {}) #POURQUOI CA MARCHE PAS ?
	#return HttpResponse("Give me a list of recommended recipes and a grocery list." )
	#return HttpResponseRedirect((reverse('foodapp:model_results'))


from .pulp.ilpmodel import foo, print_opt_recipes
def model_results(request):
	#return HttpResponse("Give me a list of recommended recipes and a grocery list." )
	list_selected_rid = print_opt_recipes()
	selected_recipes = Recipe.objects.filter(id__in=list_selected_rid).order_by('rid')
	context = {'selected_recipes' : selected_recipes}
	#return HttpResponse(output, content_type="text/plain")
	return render(request, 'foodapp/model-results.html', context)

def rank_output(request):
	# Create the formset, specifying the form and formset we want to use.
	#RankRecipeFormSet = formset_factory(RankRecipeForm, formset=BaseRankRecipeFormSet)
	RankRecipeFormSet = formset_factory(RankRecipeForm, formset=BaseFormSet)

	# Get our selected recipes from the ILP model for this user.  This is used as initial data.
	list_selected_rid = print_opt_recipes()
	selected_recipes = Recipe.objects.filter(id__in=list_selected_rid).order_by('rid')
	recipes_data = [{'rid': r.rid,'recipe_name': r.recipe_name, 'ranking': r.ranking} for r in selected_recipes]

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		#rankrecipe_formset = RankRecipeFormSet(request.POST, initial=recipes_data)

		rankrecipe_formset = RankRecipeFormSet(request.POST)

		if rankrecipe_formset.is_valid():
			# Save the data for each form in the formset
			new_rankings = []

			for rankrecipe_form in rankrecipe_formset:
				newranking = rankrecipe_form.cleaned_data.get('ranking')
				this_rid = rankrecipe_form.cleaned_data.get('rid')

				#if newranking:
					#new_rankings.append(UserLink(user=user, anchor=anchor, url=url))

				try:
					with transaction.atomic():
						#Replace the old ranking with the new ranking for this recipe
						this_recipe = Recipe.objects.filter(id=this_rid)
						this_recipe.ranking = newranking
						this_recipe.save(update_fields=['ranking'])

					# And notify our users that it worked
						messages.success(request, 'You have updated your ranking of this recipe.')

				except IntegrityError: #If the transaction failed
					messages.error(request, 'There was an error saving your ranking.')

	# if a GET (or any other method) we'll create a blank form
	else:
		rankrecipe_formset = RankRecipeFormSet(initial=recipes_data)

	context = {
		'rankrecipe_formset': rankrecipe_formset,
	}

	return render(request, 'foodapp/rank-output.html', context)
		
