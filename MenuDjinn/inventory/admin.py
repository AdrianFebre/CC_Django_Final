from django.contrib import admin
from .models import Ingredients, MenuItems, RecipeRequirements, Purchase

# Register your models here.
admin.site.register(Ingredients)
admin.site.register(MenuItems)
admin.site.register(RecipeRequirements)
admin.site.register(Purchase)