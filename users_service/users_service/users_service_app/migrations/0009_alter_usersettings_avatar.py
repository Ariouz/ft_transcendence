# Generated by Django 4.0.1 on 2024-11-26 15:05

from django.db import migrations, models
import users_service_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('users_service_app', '0008_alter_usersettings_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.svg', null=True, upload_to=users_service_app.models.user_directory_path),
        ),
    ]
