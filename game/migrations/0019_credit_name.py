# Generated by Django 4.0.3 on 2022-06-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='name',
            field=models.CharField(default='cred', max_length=1000),
            preserve_default=False,
        ),
    ]