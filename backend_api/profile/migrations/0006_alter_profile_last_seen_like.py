# Generated by Django 4.1 on 2022-10-11 08:10

from django.db import migrations, models
import django.db.models.deletion
import utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_contact_is_mutual_alter_profile_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_seen',
            field=models.BigIntegerField(default=1665475858333),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.BigIntegerField(default=utils.utils.current_time_in_millis)),
                ('is_liked', models.BooleanField(default=1)),
                ('who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='profile.profile')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='profile.profile')),
            ],
            options={
                'unique_together': {('who', 'whom')},
            },
        ),
    ]
