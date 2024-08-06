from django.contrib.auth.models import AbstractUser
from django.db import models

# Asosiy usermodelni sittings.py ga qushib quyish kerak AUTH_USER_MODEL = "users.CustomUser"
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="default_profile_pic.jpg")
