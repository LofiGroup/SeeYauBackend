from django.db import migrations, models
import json
from utils.file import resolve_extra


def fix_url(url: str):
    index = url.rfind("media")
    result = url[index:]
    if url.endswith("."):
        result = result + "jpg"

    return result


def get_file_path(url: str):
    index = url.rfind("media")
    return url[index+6:]


def migrate_to_extra_forwards(apps, schema_editor):
    ChatMessage = apps.get_model("chat", "ChatMessage")
    db_alias = schema_editor.connection.alias

    for message in ChatMessage.objects.using(db_alias):
        extra = message.extra
        if extra == "":
            continue

        extra_dict = json.loads(extra)
        uri = extra_dict.get("uri")

        if uri is None:
            message.extra = ""
        else:

            message.extra = resolve_extra(message.message_type, get_file_path(uri))
        message.save()


def migrate_to_extra_backwards(apps, schema_editor):
    ChatMessage = apps.get_model("chat", "ChatMessage")
    db_alias = schema_editor.connection.alias

    for message in ChatMessage.objects.using(db_alias):
        if message.extra is None or len(message.extra) == 0:
            continue

        extra = json.loads(message.extra)
        if extra.get("file_info") is None:
            old_extra = {
                "uri": None
            }
        else:
            old_extra = {
                "uri": extra["file_info"]["uri"]
            }
        message.extra = json.dumps(old_extra)
        message.save()


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0006_alter_chatmessage_extra_alter_chatmessage_message'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_to_extra_forwards,
            reverse_code=migrate_to_extra_backwards
        )
    ]
