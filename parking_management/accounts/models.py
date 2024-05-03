from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Додаткові поля користувача

class Administrator(CustomUser):
    # Додаткові поля адміністратора