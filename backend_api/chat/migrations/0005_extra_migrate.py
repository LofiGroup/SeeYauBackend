from django.db import migrations, models
import json


def migrate_to_extra_forwards(apps, schema_editor):
    ChatMessage = apps.get_model("chat", "ChatMessage")
    db_alias = schema_editor.connection.alias

    for message in ChatMessage.objects.using(db_alias):
        extra = message.extra
        new_extra = { "uri": extra }
        if message.message_type == "video":
            new_extra["thumbnail_uri"] = ""
        message.extra = json.dumps(new_extra)
        message.save()


def migrate_to_extra_backwards(apps, schema_editor):
    ChatMessage = apps.get_model("chat", "ChatMessage")
    db_alias = schema_editor.connection.alias

    for message in ChatMessage.objects.using(db_alias):
        extra = json.loads(message.extra)
        message.extra = extra["uri"]
        message.save()


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0004_remove_chatmessage_media_uri_chatmessage_extra'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_to_extra_forwards,
            reverse_code=migrate_to_extra_backwards
        )
    ]
