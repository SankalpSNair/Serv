# Generated by Django 5.0.6 on 2024-08-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_app', '0006_rename_user_house_maid_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carpenter',
            name='place',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='electrician',
            name='place',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='home_nurse',
            name='place',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='house_maid',
            name='place',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='plumber',
            name='place',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
