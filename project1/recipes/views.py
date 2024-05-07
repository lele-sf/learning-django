from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    context = {"title": "Home | Recipes", "recipes": recipes}
    return render(request, "recipes/pages/home.html", context)


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by(
            "-id"
        )
    )
    context = {
        "title": f"{recipes[0].category.name} - Category | Recipes",
        "recipes": recipes,
    }

    return render(request, "recipes/pages/home.html", context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    context = {
        "title": f"{recipe.title} | Recipes",
        "recipe": recipe,
        "is_detail": True,
    }
    return render(request, "recipes/pages/recipe-detail.html", context)


def search(request):
    search_query = request.GET.get("q")

    if not search_query:
        raise Http404("No query provided")

    return render(request, "recipes/pages/search.html", {"title": "Search | Recipes"})
