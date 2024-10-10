# Generated by Django 4.0.1 on 2024-10-10 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong_service_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PongUser',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
