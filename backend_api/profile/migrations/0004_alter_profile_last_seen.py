# Generated by Django 4.1 on 2022-10-10 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.BigIntegerField(default=1665390449210),
        ),
    ]