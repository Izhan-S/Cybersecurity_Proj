# Generated by Django 4.0.3 on 2022-06-04 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_remove_game_training_video_game_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module_segment',
            name='training_video',
        ),
        migrations.AddField(
            model_name='module_segment',
            name='video',
            field=models.FileField(null=True, upload_to='videos_uploaded', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]