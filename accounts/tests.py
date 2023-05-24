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

    def test_register_existing_username_redirect2(self):
        # Test registering with an existing username and redirecting status code from 302 to 200
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

        self.assertRedirects(
            response, reverse("register"), status_code=302, target_status_code=200
        )

    def test_register_existing_username_messages2(self):
        # Test registering with an existing username and a response message
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
            follow=True,
        )
        print(response.context["messages"])
        self.assertContains(response, "That username is taken")

    def test_register_existing_email_redirect3(self):
        # Test registering with an existing email and redirecting status code from 302 to 200
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
        self.assertRedirects(
            response, reverse("register"), status_code=302, target_status_code=200
        )

    def test_register_existing_email_messages(self):
        # Test registering with an existing email and a response message
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
            follow=True,
        )
        print(response.context["messages"])
        self.assertContains(response, "That email is being used")

    def test_register_password_mismatch_redirect4(self):
        # Test registering with mismatched passwords and redirecting status code from 302 to 200
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
        self.assertRedirects(
            response, reverse("register"), status_code=302, target_status_code=200
        )

    def test_register_password_mismatch_messages(self):
        # Test registering with mismatched passwords and a response message
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
            follow=True,
        )

        print(response.context["messages"])
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
