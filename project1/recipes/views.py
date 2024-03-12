from django.shortcuts import render
from utils.recipes.factory import make_recipe


def home(request):
    context = {'title': 'Home | Recipes', 'recipes': [make_recipe() for _ in range(9)]}
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, id):
    context = {'title': 'Detail | Recipes', 'recipe': make_recipe(), 'is_detail': True}
    return render(request, 'recipes/pages/recipe-detail.html', context)
