from django.db import models

# Create your models here.
class Sentiment(models.Model):
    text = models.CharField(max_length=5000)
    docfile = models.FileField(upload_to='upload/')
    translated_text = models.CharField(max_length=5000)
    sentiment = models.CharField(max_length=1000)
    username = models.CharField(max_length=150)

    # def save(self, *args, **kwargs):
    #     file_text = self.cvfile.open().read()
    #     self.text = file_text
    #     super(Clean, self).save(*args, **kwargs) 