# Generated by Django 4.1 on 2022-10-19 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chatuser_unique_together_delete_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='is_private',
            field=models.BooleanField(default=1),
        ),
    ]
