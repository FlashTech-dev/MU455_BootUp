# Generated by Django 3.0.8 on 2020-07-30 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200730_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentiment',
            name='username',
            field=models.CharField(default='no_user', max_length=150),
            preserve_default=False,
        ),
    ]