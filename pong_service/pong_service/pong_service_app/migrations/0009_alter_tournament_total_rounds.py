# Generated by Django 4.0.1 on 2025-02-04 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong_service_app', '0008_tournament_current_round_tournament_total_rounds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='total_rounds',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
