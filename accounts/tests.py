from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class AccountsTestCase(TestCase):
    # Invoked before each test
    def setUp(self):
        self.client = Client()

    def test_register_valid_credentials1(self):
        # Test registering with valid credentials
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "janedoe",
                "email": "janedoe@example.com",
                "password": "password123",
                "password2": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "janedoe")

    def test_register_existing_username2(self):
        # Test registering with an existing username
        User.objects.create_user(username="janedoe", password="password123")
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "janedoe",
                "email": "janedoe@example.com",
                "password": "password123",
                "password2": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("register"))
        self.assertContains(response, "That username is taken")

    def test_register_existing_email3(self):
        # Test registering with an existing email
        User.objects.create_user(
            username="existinguser", password="password123", email="janedoe@example.com"
        )
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "janedoe",
                "email": "janedoe@example.com",
                "password": "password123",
                "password2": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("register"))
        self.assertContains(response, "That email is being used")

    def test_register_password_mismatch4(self):
        # Test registering with mismatched passwords
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "username": "janedoe",
                "email": "janedoe@example.com",
                "password": "password123",
                "password2": "mismatchedpassword",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("register"), target_status_code=200)
        self.assertContains(response, "Passwords do not match")

    def test_login_valid_credentials5(self):
        # Create a user for testing login
        user = User.objects.create_user(username="janedoe", password="password123")
        response = self.client.post(
            reverse("login"),
            {
                "username": "janedoe",
                "password": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
