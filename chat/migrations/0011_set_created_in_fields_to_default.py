from django.db import migrations, models
from utils.utils import current_time_in_millis


def reset_created_in_to_default(apps, schema_editor):
    ChatUser = apps.get_model('chat', 'ChatUser')
    for row in ChatUser.objects.all():
        row.joined_in = current_time_in_millis()
        row.save()

    ChatMessage = apps.get_model('chat', 'ChatMessage')
    for row in ChatMessage.objects.all():
        row.created_in = current_time_in_millis()
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_alter_chatmessage_created_in_and_more'),
    ]

    operations = [
        migrations.RunPython(reset_created_in_to_default)
    ]
