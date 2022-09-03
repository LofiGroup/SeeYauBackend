import time


def current_time_in_millis():
    return time.time_ns() // 1_000_000


def parse_query_string(query):
    return dict((x.split('=') for x in query.decode().split("&")))
