# Generated by Django 5.2 on 2025-05-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_app', '0017_remove_advertiser_api_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
            ],
        ),
    ]
