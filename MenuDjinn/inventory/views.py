from re import L
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredients, MenuItems, RecipeRequirements, Purchase
from .forms import IngredientAddForm, MenuAddForm, PurchaseForm, RecipeAddForm
import numpy as np

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

# temp - trying to avoid creating a new...something
# very, very likely not the ideal way to do this  - check both projects for ideas
def temp_purchase_list(request):
    context = {}
    # pull purchases
    all_purchases = Purchase.objects.all()
    # define rev, loss -> profit
    revenue = 0.0
    cost = 0.0

    for purchase in all_purchases:
        # first, revenue, since it's easy
        purchase_revenue = purchase.menu_item.item_price * purchase.order_quantity
        revenue += purchase_revenue

        # now, cost; because one menu item per purchase:
        purchase_item = purchase.menu_item
        purchase_recipe = RecipeRequirements.objects.filter(menu_item=purchase_item)  # sub-optimal?
        purchase_quantity = purchase.order_quantity 
        # now to sum on ingredient cost
        purchase_cost = sum([item.ingredient.price_per_unit * item.ingredient_quantity * purchase_quantity 
                            for item in purchase_recipe])  # might work
        cost += purchase_cost

    temp = []
    # simplest possible test
    for purchase in [all_purchases[0]]:
        iter_temp = [item.ingredient for item in RecipeRequirements.objects.filter(menu_item=purchase.menu_item)]
        #purchase.reciperequirements_set.all()
        temp.append(iter_temp)

    revenue, cost = round(revenue, 2), round(cost, 2)
    profit = revenue - cost

    context['revenue'] = f'${revenue}'
    context['cost'] = f'${cost}'
    context['profit'] = f'${profit}'
    context['temp'] = temp
    return render(request, 'inventory/profit_and_loss.html', context)

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