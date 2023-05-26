from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import reverse

from contacts.models import Contact
from contacts.views import contact


class ContactsTestCase(TestCase):
    # A mock request object that is invoked before each test
    def setUp(self):
        self.factory = RequestFactory()
        self.listing_id = 1
        self.listing = "A famous street"
        self.name = "Viktor Olsson"
        self.email = "viktor@example.com"
        self.phone = "1234567"
        self.message = "Test message"
        self.user_id = 1
        self.realtor_email = "realtor@example.com"

    def test_authenticated_user_no_inquiry1(self):
        # Test checking with an authenticated user who has not made an inquiry
        request = self.factory.post(reverse("contact"))
        request.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        request.POST = {
            "listing_id": self.listing_id,
            "listing": self.listing,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "message": self.message,
            "user_id": self.user_id,
            "realtor_email": self.realtor_email,
        }
        request = RequestFactory().get("/listings/1")
        contact(request)

    def test_authenticated_user_inquiry_posted2(self):
        # Test checking an authenticated user that has already made an inquiry
        request = self.factory.post(reverse("contact"))
        request.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Create an existing contact object for the authenticated user and listing
        Contact.objects.create(listing_id=self.listing_id, user_id=self.user_id)
        request.POST = {
            "listing_id": self.listing_id,
            "listing": self.listing,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "message": self.message,
            "user_id": self.user_id,
            "realtor_email": self.realtor_email,
        }

        request = RequestFactory().get("/listings/1")
        contact(request)

        # Verify no new contact object was created
        contacts = Contact.objects.filter(
            listing_id=self.listing_id, user_id=self.user_id
        )
        self.assertEqual(contacts.count(), 1)  # Only the existing contact should exist

        # Clean up by deleting the created contact object
        contacts.delete()
