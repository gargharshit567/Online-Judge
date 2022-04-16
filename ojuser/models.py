from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Ojuser(AbstractUser):

    name= models.CharField(max_length= 20)
    email= models.CharField(max_length= 100, unique= True)
    password= models.CharField(max_length= 255)
    username= models.CharField(max_length=255,unique= True)

    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS= []
    
    def __str__(self):
        return self.name
    
