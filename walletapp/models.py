from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,blank=True,default=True,on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username