from django.db import models


# Create your models here.
class RegisterUserModel(models.Model):
    # fields of the model
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20, unique=True)
    password2 = models.CharField(max_length=20)

    # rename the instance of the model with their username
    def __str__(self):
        return self.username
