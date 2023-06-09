from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form


# Create a form class
class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", min_length=5, max_length=150)
    email = forms.CharField(label="Email", widget=forms.EmailInput())
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(), help_text=""
    )
    password2 = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput(), help_text=""
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise forms.ValidationError("That username is taken")
        return username

    def email_clean(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise forms.ValidationError("Email Already Exist")
        return email

    def clean_password2(self):
        password = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password != password2:
            raise forms.ValidationError("Password don't match")
        return password2


# Creating a form to add a user
form = RegisterForm()
