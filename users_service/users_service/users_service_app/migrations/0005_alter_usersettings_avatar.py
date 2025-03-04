# Generated by Django 4.0.1 on 2024-08-05 12:51

from django.db import migrations, models
import users_service_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('users_service_app', '0004_usersettings_status_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=users_service_app.models.user_directory_path),
        ),
    ]
