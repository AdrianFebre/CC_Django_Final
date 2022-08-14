from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # core urls
    path('ingredients/', views.IngredientsList.as_view(), name='ingredientslist'),
    path('menus/', views.MenuList.as_view(), name='menulist'),
    path('recipes/', views.RecipeList.as_view(), name='recipelist'),
    path('purchases/', views.PurchaseList.as_view(), name='purchaselist'),
    # basic create/edit
    path('ingredients/create/', views.IngredientsCreate.as_view(), name='ingredientscreate'),
    path('ingredients/update/<pk>', views.IngredientsUpdate.as_view(), name='ingredientsupdate'),
    path('ingredients/delete/<pk>', views.IngredientsDelete.as_view(), name='ingredientsdelete'),
    path('menus/create/', views.MenuCreate.as_view(), name='menucreate'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipecreate'),
    path('purchases/create/', views.PurchaseCreate.as_view(), name='purchasecreate'),
    # tougher - profit and loss
    path('profit-and-loss/', views.temp_purchase_list, name='profitandloss'),
    path('pandl-class-based', views.ProfitAndLoss.as_view(), name='classedprofitandloss'),
    # login/logout
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path('accounts/logout/', views.logout_view, name='logout'),
    #path('accounts/login/', views.login_view, name='login'),  # manual version of login, doesn't at the moment
]