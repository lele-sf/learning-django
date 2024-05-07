from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # Test if the view functions are correct
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func, views.search)

    # Test if the views return the correct status code
    def test_recipe_home_view_status_code_200(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_status_code_200(self):
        self.make_recipe()
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_status_code_200(self):
        self.make_recipe()
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)

    # Test if the views return the correct template
    def test_recipe_home_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_category_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_detail_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertTemplateUsed(response, "recipes/pages/recipe-detail.html")

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse("recipes:search") + "?q=test")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    # Test if the views handle non-existing recipes correctly
    def test_recipe_home_view_no_recipes(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes found")

    def test_recipe_category_view_recipes_not_found(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 100})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_recipe_not_found(self):
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_raises_404_if_no_query(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    # Test if the views return the correct recipes
    def test_recipe_home_template_loads_recipes(self):
        new_user = self.make_user(username="newuser", password="12345")
        self.make_recipe(
            title="New Recipe Title",
            author_data=new_user,
        )

        response = self.client.get(reverse("recipes:home"))
        response_recipes = response.context["recipes"]
        content = response.content.decode("utf-8")

        self.assertEqual(len(response_recipes), 1)
        self.assertEqual(response_recipes[0].title, "New Recipe Title")
        self.assertEqual(response_recipes[0].author, new_user)
        self.assertIn("New Recipe Title", content)
        self.assertIn("Test Description", content)
        self.assertIn("30 minutes", content)

    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        response_recipes = response.context["recipes"]
        content = response.content.decode("utf-8")

        self.assertEqual(response_recipes[0].title, "Test Title")
        self.assertIn("Test Description", content)

    def test_recipe_detail_template_loads_recipe(self):
        detail_title = "Detail Recipe Title"
        self.make_recipe(title=detail_title)

        response = self.client.get(reverse("recipes:recipe", kwargs={"id": 1}))
        content = response.content.decode("utf-8")

        self.assertIn(detail_title, content)

    # Test if the views handle unpublished recipes correctly
    def test_recipe_home_template_does_not_load_unpublished_recipes(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))
        response_recipes = response.context["recipes"]
        content = response.content.decode("utf-8")

        self.assertEqual(len(response_recipes), 0)
        self.assertIn("No recipes found", content)

    def test_recipe_category_template_does_not_load_unpublished_recipes(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_does_not_load_unpublished_recipe(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:recipe", kwargs={"id": recipe.id}))
        self.assertEqual(response.status_code, 404)
