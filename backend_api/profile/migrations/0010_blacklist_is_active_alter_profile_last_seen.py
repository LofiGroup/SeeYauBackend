# Generated by Django 4.1 on 2022-10-25 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0009_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklist',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.BigIntegerField(default=1666708137935),
        ),
    ]
