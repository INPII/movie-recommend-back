# Generated by Django 4.2.8 on 2024-05-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
