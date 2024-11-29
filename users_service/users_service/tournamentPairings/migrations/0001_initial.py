# Generated by Django 4.2.16 on 2024-11-08 07:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentPairingData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tournament_id', models.CharField(max_length=60)),
                ('round_id', models.CharField(blank=True, max_length=60, null=True)),
                ('linkToJoin', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('player1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1_id', to='users.user')),
                ('player2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2_id', to='users.user')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner_id', to='users.user')),
            ],
        ),
    ]
