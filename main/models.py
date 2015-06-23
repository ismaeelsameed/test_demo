from django.db import models
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)