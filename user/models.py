from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    contact_number = models.CharField(
        max_length=15, blank=True, null=True, unique=True, verbose_name="Phone Number"
    )
    gender = models.CharField(
        max_length=10, choices=[("M", "Male"), ("F", "Female")], null=True, blank=True
    )
    user_image = models.ImageField(null=True, blank=True, upload_to="media/")

    def __str__(self):
        return f"{self.username}"
