# Generated by Django 4.0.3 on 2022-06-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_remove_module_segment_training_video_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='module_question',
            name='option_A',
            field=models.CharField(default='An impersonator trying to get your information (vishing/smishing)', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module_question',
            name='option_B',
            field=models.CharField(default='A man-in-the-middle trying to steal your information or infect your system with malware (Juice jacking)', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module_question',
            name='option_C',
            field=models.CharField(default='Another piece of your digital identity left in the cyber world (Digital footprint)', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module_question',
            name='right_option',
            field=models.CharField(default='A', max_length=1),
        ),
    ]