# Generated by Django 4.0.3 on 2022-04-18 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_game_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='scenario',
            field=models.TextField(max_length=1000),
        ),
    ]