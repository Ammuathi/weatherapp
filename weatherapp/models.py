from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
  def __str__(self):
     return self.username
    # username = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # password= models.CharField(max_length=100)
    