# Generated by Django 5.2 on 2025-04-27 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_app', '0005_sportsman_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportsman',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
