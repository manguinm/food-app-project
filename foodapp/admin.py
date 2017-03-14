from django.contrib import admin

# Register your models here.
from .models import Ingredient, Recipe, Relationship

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Relationship)