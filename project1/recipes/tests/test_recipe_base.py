from django.test import TestCase
from recipes.models import Recipe, Category
from django.contrib.auth.models import User


class RecipeTestBase(TestCase):
    def setUp(self):
        super().setUp()

    def make_user(self, username="testuser", password="12345"):
        return User.objects.create_user(username=username, password=password)

    def make_category(self, name="Test Category"):
        return Category.objects.create(name=name)

    def make_recipe(
        self,
        title="Test Title",
        description="Test Description",
        slug="test-recipe-1",
        preparation_time=30,
        preparation_time_unit="minutes",
        servings=4,
        servings_unit="servings",
        preparation_steps="Test preparation steps",
        is_published=True,
        author_data=None,
        category_data=None,
    ):
        if author_data is None:
            author_data = self.make_user()
        if category_data is None:
            category_data = self.make_category()

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            is_published=is_published,
            author=author_data,
            category=category_data,
        )
