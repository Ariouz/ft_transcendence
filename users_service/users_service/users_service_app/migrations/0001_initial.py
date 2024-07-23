# Generated by Django 5.0.6 on 2024-07-23 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('token', models.CharField(max_length=128, unique=True)),
                ('fullname', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('avatar', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=32)),
            ],
        ),
    ]
