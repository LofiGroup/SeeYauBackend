# Generated by Django 4.1 on 2022-08-23 10:13

import chat.models.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
        ('chat', '0007_alter_chatmessage_created_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatuser',
            name='joined_in',
            field=models.BigIntegerField(default=chat.models.models.get_current_time),
        ),
        migrations.AlterField(
            model_name='chatuser',
            name='user',
            field=models.ForeignKey(on_delete=models.SET(chat.models.models.get_sentinel_profile), to='profile.profile'),
        ),
    ]
