# Generated by Django 4.0.3 on 2022-04-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_game_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='intro',
            field=models.TextField(),
        ),
    ]
