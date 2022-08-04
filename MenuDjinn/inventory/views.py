from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredients, MenuItems, RecipeRequirements, Purchase
from .forms import IngredientAddForm, MenuAddForm, PurchaseForm, RecipeAddForm

# Create your views here.

# very basic home, for now
def home(request):
    context = {}  # blank for now
    return render(request, 'inventory/home.html', context)

# I think...huh...I make my custom functions here (allowing me to play with instances), and then
# call them in views below

'''
List Views
'''
# inventory view
class IngredientsList(ListView):
    model = Ingredients
    template_name = 'inventory/ingredients_list.html'

# menu view
class MenuList(ListView):
    model = MenuItems
    template_name = 'inventory/menu_list.html'

# RecipeRequirements view
class RecipeList(ListView):
    model = RecipeRequirements
    template_name = 'inventory/recipe_list.html'

# list of purchases - could prob take a date as a param, default=today() or something
class PurchaseList(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'

'''
Editing Views
'''
# ingredient create and delete
class IngredientsCreate(CreateView):
    model = Ingredients
    template_name = 'inventory/ingredients_create_form.html'
    '''
    fields = ['ingredient_name', 'quantity', 'price_per_unit', 'units']
    success_url = 'ingredients/list/'  # these don't work right now
    '''
    # now, with form added
    form_class = IngredientAddForm

class IngredientsUpdate(UpdateView):
    model = Ingredients
    template_name = 'inventory/ingredients_update_form.html'
    fields = ['ingredient_name', 'quantity', 'price_per_unit', 'units']
    success_url = '..'

class IngredientsDelete(DeleteView):
    model = Ingredients
    template_name = 'inventory/ingredients_delete_form.html'
    success_url = '..'

# menu and recipe create
class MenuCreate(CreateView):
    model = MenuItems
    template_name = 'inventory/menu_create_form.html'
    form_class = MenuAddForm

class RecipeCreate(CreateView):
    model = RecipeRequirements
    template_name = 'inventory/recipe_create_form.html'
    form_class = RecipeAddForm

# I think it'd be nice to make purchases w/o admin priveleges
class PurchaseCreate(CreateView):
    model = Purchase
    template_name = 'inventory/purchase_form.html'
    '''
    fields = ['customer_name', 'menu_item', 'order_quantity']
    success_url = '..'
    '''
    form_class = PurchaseForm