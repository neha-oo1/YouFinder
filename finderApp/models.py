from django.db import models

# Create your models here.

# Database of image to compare other images
class SImg(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='simage', blank=True)

# Database of images to be compared
class MulImg(models.Model):
    name = models.CharField(max_length=255)
    images = models.FileField(upload_to='images', blank=True)