from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingredients/', views.IngredientsList.as_view(), name='ingredientslist'),
    path('menus/', views.MenuList.as_view(), name='menulist'),
    path('recipes/', views.RecipeList.as_view(), name='recipelist'),
    path('purchases/', views.PurchaseList.as_view(), name='purchaselist'),
    path('ingredients/create/', views.IngredientsCreate.as_view(), name='ingredientscreate'),
    path('ingredients/update/<pk>', views.IngredientsUpdate.as_view(), name='ingredientsupdate'),
    path('ingredients/delete/<pk>', views.IngredientsDelete.as_view(), name='ingredientsdelete'),
    path('menus/create/', views.MenuCreate.as_view(), name='menucreate'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipecreate'),
    path('purchases/create/', views.PurchaseCreate.as_view(), name='purchasecreate'),
    path('profit-and-loss/', views.temp_purchase_list, name='profitandloss'),
]