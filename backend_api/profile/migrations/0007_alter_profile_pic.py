# Generated by Django 4.1 on 2022-09-16 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_rename_img_url_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='blank_profile_image.jpg', upload_to='images/profile/'),
        ),
    ]
