from django import forms
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from foodapp.models import Recipe, Ingredient


class RankRecipeForm(forms.ModelForm):
	#recipe_name = forms.CharField(widget=forms.HiddenInput(), required=False)

	# intialize the data maybe ??

	# http://stackoverflow.com/questions/6472269/django-modelform-with-initial-data-not-shown-on-redisplay

	class Meta:
		model = Recipe
		fields = ['rid', 'recipe_name', 'ranking']
		widgets = {'rid': forms.HiddenInput(), 'recipe_name' : forms.TextInput(attrs={'readonly':'readonly'}), 
		'ranking' : forms.NumberInput(attrs={'min': 0, 'max': 10})}
		exclude = ('ingredients','number_steps','instructions' ) # exclude everything but ranking!


#RankRecipeFormSet = formset_factory(RankRecipeForm) 

class BaseRankRecipeFormSet(BaseFormSet):
	def clean(self):
		"""
		Adds validation 
		"""
		if any(self.errors):
			return None

		for form in self.forms:
			if form.cleaned_data:
				ranking = form.cleaned_data['ranking']

		# Check that all recipes have a ranking 
		if not ranking:
			raise forms.ValidationError(
				'All recipes must have a ranking.',
				code = 'missing_ranking')
	