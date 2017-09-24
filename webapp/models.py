from django.db import models

# Create your models here.

class Production(models.Model):
    pId = models.CharField(max_length=100)
    pName = models.CharField(max_length=20)
    pDescribe = models.CharField(max_length=50)
    pIconPath = models.CharField(max_length=100)
    pPrice = models.FloatField(max_length=5)

    def __str__(self):
        return self.pName

class UserInfo(models.Model):
    user_name = models.CharField(max_length=8)
    user_password = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=15)
    user_address = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name