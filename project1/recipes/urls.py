from django.urls import path
from recipes import views

# recipes:home
app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('recipes/search/', views.search, name='search'),  # Search page
    path('recipes/category/<int:category_id>/', views.category, name='category'),  # Category page
    path('recipes/<int:id>/', views.recipe, name='recipe'),  # Recipe page
]
