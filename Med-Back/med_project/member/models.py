from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class UserMed(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User ,on_delete=models.CASCADE, null=False , default=None)
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100,null=False)
    cin = models.CharField(max_length=8,unique=True,null=False)
    email = models.EmailField(null=False)
    phone_number = models.CharField(max_length=8)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    original_institute = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True, null=True,blank=True)
    secretword=models.CharField(max_length=100, null=False , default=None)




    