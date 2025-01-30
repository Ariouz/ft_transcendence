# Generated by Django 4.0.1 on 2025-01-30 21:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pong_service_app', '0003_tournament_tournamentmatch_tournamentparticipant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tournament_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
