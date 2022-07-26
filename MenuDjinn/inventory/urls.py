from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingredients/list', views.IngredientsList.as_view(), name='ingredientslist'),
    path('menu/list/', views.MenuList.as_view(), name='menulist'),
    path('recipe/list', views.RecipeList.as_view(), name='recipelist'),
    path('purchase/list', views.PurchaseList.as_view(), name='purchaselist'),
    path('ingredients/create', views.IngredientsCreate.as_view(), name='ingredientscreate'),
    path('ingredients/update/<pk>', views.IngredientsUpdate.as_view(), name='ingredientsupdate'),
    path('ingredients/delete/<pk>', views.IngredientsDelete.as_view(), name='ingredientsdelete'),
    path('purchase/create', views.PurchaseCreate.as_view(), name='purchasecreate'),
]