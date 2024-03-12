from django.urls import path
from recipes import views

# recipes:home
app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('recipes/<int:id>/', views.recipe, name='recipe'),  # Recipe page
]
