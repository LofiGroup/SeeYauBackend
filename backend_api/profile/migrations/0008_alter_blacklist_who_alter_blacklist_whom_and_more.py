# Generated by Django 4.1 on 2022-10-19 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_alter_profile_last_seen_blacklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklist',
            name='who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blacklist', to='profile.profile'),
        ),
        migrations.AlterField(
            model_name='blacklist',
            name='whom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_blacklist', to='profile.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.BigIntegerField(default=1666189712397),
        ),
    ]
