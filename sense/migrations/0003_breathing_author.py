# Generated by Django 3.2 on 2022-10-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sense', '0002_meditation_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='breathing',
            name='author',
            field=models.CharField(default='UpSense Team', max_length=128),
        ),
    ]