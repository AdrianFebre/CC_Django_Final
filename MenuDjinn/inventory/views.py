from re import L
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredients, MenuItems, RecipeRequirements, Purchase, TimedStrings
from .forms import IngredientAddForm, MenuAddForm, PurchaseForm, RecipeAddForm, TimedStringAddForm
from django.urls import reverse
# bonus
import numpy as np
import pandas as pd
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

# very basic home, for now
@login_required
def home(request):
    context = {}  # blank for now
    return render(request, 'inventory/home.html', context)

# I think...huh...I make my custom functions here (allowing me to play with instances), and then
# call them in views below

'''
List Views
'''
# inventory view
class IngredientsList(LoginRequiredMixin, ListView):
    model = Ingredients
    template_name = 'inventory/ingredients_list.html'

# menu view
class MenuList(LoginRequiredMixin, ListView):
    model = MenuItems
    template_name = 'inventory/menu_list.html'

# RecipeRequirements view
class RecipeList(LoginRequiredMixin, ListView):
    model = RecipeRequirements
    template_name = 'inventory/recipe_list.html'

# list of purchases - could prob take a date as a param, default=today() or something
class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'

# new - for click event testing; see below for creation view
class TimedStringsList(LoginRequiredMixin, ListView):
    model = TimedStrings
    template_name = 'inventory/timed_string_list.html'

# temp - trying to avoid creating a new...something
# very, very likely not the ideal way to do this  - check both projects for ideas
# complete - it works, but see the class-based implementation below
@login_required
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

# and the class-based version of that, per the example code
class ProfitAndLoss(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/p_and_l_class_based.html'

    # need total costs, total rev, and the diff as profit
    def total_cost_and_rev(self):
        # as above
        cost, revenue = 0.0, 0.0
        # new - we're making a dataframe to break things down by date
        # we want a dataframe w/ an id, rev, cost, profit, and the date
        pandl_by_date_df = pd.DataFrame(columns=['purchase_id', 'cost', 'revenue', 
                                                 'profit', 'date'])
        all_purchases = Purchase.objects.all()

        for purchase in all_purchases:
            purchase_revenue = purchase.menu_item.item_price * purchase.order_quantity
            revenue += purchase_revenue

            purchase_item = purchase.menu_item
            purchase_recipe = RecipeRequirements.objects.filter(menu_item=purchase_item)  # sub-optimal?
            purchase_quantity = purchase.order_quantity 
            # now to sum on ingredient cost
            purchase_cost = sum([item.ingredient.price_per_unit * item.ingredient_quantity * purchase_quantity 
                                for item in purchase_recipe])
            cost += purchase_cost
            # and now we toss the relevant data into our dataframe
            purchase_id = purchase.pk  # might work?
            # there's a way more elegant solution here with two lists and zip, but for legibility:
            purchase_df_row = {'purchase_id': purchase_id, 'cost': purchase_cost,
                               'revenue': purchase_revenue, 'profit': 0, 'date': purchase.purchase_timestamp}
            pandl_by_date_df = pandl_by_date_df.append(purchase_df_row, ignore_index=True)

        profit = revenue - cost
        pandl_by_date_df['profit'] = pandl_by_date_df.revenue - pandl_by_date_df.cost  # should work
        # note: I think I'd have to add in a groupby(date) myself
        profit_by_date_df = pandl_by_date_df.groupby('date').profit.sum().reset_index()
        return cost, revenue, profit, pandl_by_date_df.to_html(), profit_by_date_df.to_html()  # internet trick - studygyaan

    # mostly cloned from elMolo example
    def get_context_data(self):
        # base context
        context = super().get_context_data()
        # custom context
        context['cost'], context['revenue'], context['profit'],\
            context['pandl_by_date_df'], context['profit_by_date_df'] = self.total_cost_and_rev()
        return context

'''
Editing Views
'''
# ingredient create and delete
class IngredientsCreate(LoginRequiredMixin, CreateView):
    model = Ingredients
    template_name = 'inventory/ingredients_create_form.html'
    '''
    fields = ['ingredient_name', 'quantity', 'price_per_unit', 'units']
    success_url = 'ingredients/list/'  # these don't work right now
    '''
    # now, with form added
    form_class = IngredientAddForm

class IngredientsUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredients
    template_name = 'inventory/ingredients_update_form.html'
    fields = ['ingredient_name', 'quantity', 'price_per_unit', 'units']
    success_url = '..'

class IngredientsDelete(LoginRequiredMixin, DeleteView):
    model = Ingredients
    template_name = 'inventory/ingredients_delete_form.html'
    success_url = '..'

# menu and recipe create
class MenuCreate(LoginRequiredMixin, CreateView):
    model = MenuItems
    template_name = 'inventory/menu_create_form.html'
    form_class = MenuAddForm

class RecipeCreate(LoginRequiredMixin, CreateView):
    model = RecipeRequirements
    template_name = 'inventory/recipe_create_form.html'
    form_class = RecipeAddForm

# I think it'd be nice to make purchases w/o admin priveleges
class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'inventory/purchase_form.html'
    '''
    fields = ['customer_name', 'menu_item', 'order_quantity']
    success_url = '..'
    '''
    form_class = PurchaseForm

# first pass - do it the "easy" way with forms.py
'''
class TimedStringsCreate(LoginRequiredMixin, CreateView):
    model = TimedStrings
    template_name = 'inventory/timed_string_create_form.html'
    form_class = TimedStringAddForm
'''
# second pass - a custom function - it works!!
def timed_strings_create(request):
  # Add your code below:
  if request.method == "POST":
    newSession = TimedStrings()
    newSession.session_name = request.POST['session_name']
    newSession.timestamp = datetime.now()  # here's the magic
    newSession.save()
    return HttpResponseRedirect(reverse('timedstringslist'))
  return render(request, 'inventory/timed_string_create_form.html')

# login/logout - just copy pasta'ing so far
# login is broken - fix 1 per the internet: request.post[] -> request.POST.get()
# fix 2 - use the standard views, adding this to urls: path('accounts/', include('django.contrib.auth.urls'))
'''
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return
    else:
        return HttpResponse('ruh roh')
'''

def logout_view(request):
  logout(request)
  return redirect('home')