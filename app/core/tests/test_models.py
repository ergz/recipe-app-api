"""
Tests for Models
"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

class ModelTest(TestCase):
    """ Test Models """

    def test_create_user_with_email_succesful(self):
        email = "test@example.com"
        password = "testpass"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test new email user is normalized"""

        sample_email = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"]
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "pass123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser("test@example.com", "test123")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):
        """Test creating a Recipe is succesfull"""

        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpassword",
        )

        recipe = models.Recipe.objects.create(
            user=user, 
            title="Sample Recipe Name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description"
        )

        self.assertEqual(str(recipe), recipe.title)