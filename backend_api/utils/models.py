from ninja import Schema
from django.db.models import ObjectDoesNotExist


class ErrorMessage(Schema):
    error_message: str

    @staticmethod
    def build(message: str):
        return {"error_message": message}


def get_or_null(query):
    try:
        return query.get()
    except ObjectDoesNotExist:
        return None
