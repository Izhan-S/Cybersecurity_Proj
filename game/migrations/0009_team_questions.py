# Generated by Django 4.0.3 on 2022-04-18 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_alter_game_image_alter_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='questions',
            field=models.ManyToManyField(to='game.question'),
        ),
    ]
