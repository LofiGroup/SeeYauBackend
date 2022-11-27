import time
from django.conf import settings


IS_ONLINE = 5555555555555


def current_time_in_millis():
    return time.time_ns() // 1_000_000


def parse_query_string(query):
    if query == b'':
        return dict()
    return dict((x.split('=') for x in query.decode().split("&")))


def resolve_media_url(url):
    if url is None or url == "":
        return ""

    domain_name = settings.DOMAIN_NAME
    media_url = settings.MEDIA_URL

    return f"https://{domain_name}{media_url}{url}"


def entries_in_list(elements: list, array: list) -> bool:
    for a in array:
        for elem in elements:
            if a == elem:
                return True
    return False
