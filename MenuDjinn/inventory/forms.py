from django import forms
from .models import Ingredients, MenuItems, RecipeRequirements, Purchase

class IngredientAddForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ('ingredient_name', 'quantity', 'price_per_unit', 'units')

class MenuAddForm(forms.ModelForm):
    class Meta:
        model = MenuItems
        fields = ('item_name', 'item_description', 'item_price')

class RecipeAddForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirements
        fields = ('menu_item', 'ingredient', 'ingredient_quantity')

class PurchaseForm(forms.ModelForm):

    # this allows me to pass in purchase time using the purchase() function
    #purchase_timestamp = forms.CharField(required=False)

    class Meta:
        model = Purchase
        fields = ('customer_name', 'menu_item', 'order_quantity')
        #exclude = ['purchase_price', 'purchase_timestamp']  # alt, less secure/clean