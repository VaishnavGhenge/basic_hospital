from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    line1 = models.TextField()
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    pincode = models.PositiveIntegerField()

class Doctor(models.Model):
    _id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    profilepic = models.ImageField(upload_to='user/doctor/profile/', default='user/default.png')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Patient(models.Model):
    _id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    profilepic = models.ImageField(upload_to='user/patient/profile/', default='user/default.png')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='postimages/')
    category = models.CharField(max_length=100)
    status = models.CharField(default='draft', max_length=100)
    summary = models.TextField()
    content = models.TextField()
