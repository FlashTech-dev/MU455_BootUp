from django.db import models

# Create your models here.
class Sentiment(models.Model):
    text = models.CharField(max_length=5000)