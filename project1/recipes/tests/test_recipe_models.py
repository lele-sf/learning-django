from django.core.exceptions import ValidationError
from parameterized import parameterized
from .test_recipe_base import RecipeTestBase, Recipe


class CategoryModelTest(RecipeTestBase):
    def setUp(self):
        super().setUp()
        self.category = self.make_category()

    def test_category_name_max_length(self):
        self.category.name = "a" * 61
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_str_method(self):
        self.assertEqual(str(self.category), self.category.name)


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        super().setUp()
        self.recipe = self.make_recipe()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name="Test Default Category"),
            author=self.make_user(username="newuser"),
            title="Test Title",
            description="Test Description",
            slug="test-recipe-no-defaults",
            preparation_time=30,
            preparation_time_unit="minutes",
            servings=4,
            servings_unit="servings",
            preparation_steps="Test preparation steps",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, "a" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_preparation_steps_is_html_false_by_default(self):
        new_recipe = self.make_recipe_no_defaults()
        self.assertFalse(new_recipe.preparation_steps_is_html)

    def test_is_published_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published)

    def test_str_method(self):
        self.assertEqual(str(self.recipe), self.recipe.title)
