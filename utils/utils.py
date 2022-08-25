import time


def current_time_in_millis():
    return time.time_ns() // 1_000_000
