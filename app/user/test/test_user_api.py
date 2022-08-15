"""
Tests for the User API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")

def create_user(**params):
    """ Create and return new user """
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """ Tests the public features of User API """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Tests creating a user is succesful """
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Tests that attempting to create user with existing
        email will correctly error out"""

        payload = {
            "email": "test@example.com",
            "password": "testpas123",
            "name": "Test Name"
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Error returned if password in too short"""
        payload = {
            "email": "test@example.com",
            "password": "t",
            "name": "Test Name"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

