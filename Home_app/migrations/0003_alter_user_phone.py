# Generated by Django 5.0.6 on 2024-08-05 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home_app', '0002_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
