from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("femal", "Female")
    class LanguageChoices(models.TextChoices):
        KOREAN = ("kr", "Korean")
        ENGLISH = ("en", "English")
    class CurrencyChoices(models.TextChoices):
        KRW = ("krw", "KRW")
        USD = ("usd", "USD")
        
    first_name = models.CharField(
        max_length=150, 
        editable=False
        )
    last_name = models.CharField(
        max_length=150, 
        editable=False
        )
    avatar = models.URLField(
        default = ""
    )
    name = models.CharField(
        max_length=150, 
        default =""
        )
    is_host = models.BooleanField(
        default=False
        )
    gender = models.CharField(
        max_length=10, 
        choices=GenderChoices.choices
        )
    language = models.CharField(
        max_length=2, 
        choices=LanguageChoices.choices
        )
    currency = models.CharField(
        max_length=3, 
        choices=CurrencyChoices.choices
        )
    
