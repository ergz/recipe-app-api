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

from recipe.serializers import RecipeSerializer


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