# Generated by Django 3.0.8 on 2020-08-02 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_sentiment_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentiment',
            name='docfile',
            field=models.FileField(default='sa', upload_to='upload/'),
            preserve_default=False,
        ),
    ]