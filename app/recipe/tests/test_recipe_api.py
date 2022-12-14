"""
Test for Recipe API
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer, 
    RecipeDetailSerializer
)


RECIPE_URL = reverse("recipe:recipe-list")

def detail_url(recipe_id):
    return reverse("recipe:recipe-detail", args=[recipe_id])

def create_recipe(user, **params):
    """Create a recipe"""

    defaults = {
        "title": "Sample Title", 
        "time_minutes": 22,
        "price": Decimal("6.77"),
        "description": "A sample description",
        "link": "http://example.com/recipe.pdf"
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITest(TestCase):
    """Test the public Recipe API"""
    
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth required for Recipe API"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """Test the private Recipe API"""
        
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@example.com", "testpass123")
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """Test retrive recipe"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        # get the two recipes that were created above, and 
        # order them my decreasing ID
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to just authenticated user"""

        others_user = get_user_model().objects.create_user("other@example.com", "testpass1234")

        create_recipe(user=self.user)
        create_recipe(user=others_user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail"""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_recipe(self):
        """Test create a recipe"""

        payload = {
            "title": "Sample Recipe", 
            "time_minutes": 30,
            "price": Decimal("5.99"),
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data["id"])
        
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)


