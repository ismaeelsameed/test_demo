from django.db import models

# Create your models here.


# Create your models here.
from django_elasticsearch.models import EsIndexable


class Post(EsIndexable, models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)