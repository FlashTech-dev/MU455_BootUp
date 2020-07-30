from django.db import models

# Create your models here.
class Sentiment(models.Model):
    text = models.CharField(max_length=5000)
    translated_text = models.CharField(max_length=5000)
    sentiment = models.CharField(max_length=1000)
    username = models.CharField(max_length=150)