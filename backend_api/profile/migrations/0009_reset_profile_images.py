from django.db import migrations
from utils.utils import current_time_in_millis


def reset_profile_images_to_default(apps, schema_editor):
    Profile = apps.get_model('profile', 'Profile')
    for row in Profile.objects.all():
        row.img_url = "images/profile/blank.png"
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_rename_pic_profile_img_url'),
    ]

    operations = [
        migrations.RunPython(reset_profile_images_to_default)
    ]