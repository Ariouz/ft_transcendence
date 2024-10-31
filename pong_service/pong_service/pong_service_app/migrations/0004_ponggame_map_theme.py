# Generated by Django 4.0.1 on 2024-10-31 09:22

from django.db import migrations, models
import pong_service_app.api.themes


class Migration(migrations.Migration):

    dependencies = [
        ('pong_service_app', '0003_ponggame_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponggame',
            name='map_theme',
            field=models.JSONField(default=pong_service_app.api.themes.get_default_theme),
        ),
    ]
