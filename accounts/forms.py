from django import forms
from django.contrib.auth.models import User

from .models import RegisterUserModel


# Create a form class
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = RegisterUserModel
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        widgets = {
            "password": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }

    def clean_password2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]
        if password != password2:
            raise forms.ValidationError("Password do not match")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("That username is taken")

    def clean_email(self):
        email = self.data.get("email") and self.cleaned_data["email"]
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("That email is being used")


# Creating a form to add a user
form = RegisterUserForm()
