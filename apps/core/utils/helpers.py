from datetime import time


def time_to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute


def minutes_to_time(minutes: int) -> time:
    return time(minutes // 60, minutes % 60)
