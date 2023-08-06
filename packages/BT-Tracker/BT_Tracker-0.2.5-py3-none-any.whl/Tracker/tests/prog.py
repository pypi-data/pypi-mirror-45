import time

from functools import wraps

from ..event import status


def spin_progress(title: str) -> NoReturn:
    index = 0
    while True:
        print(f"  {'⠹⠸⠼⠴⠦⠧⠇⠏⠋⠙'[index % 10]} {title}", end="\r", flush=True)
        time.sleep(0.07)
        index += 1
        if status.finished:
            break


def info(func):
    @wraps(func)
    def warpper(*args, **kwargs):
        func(*args, **kwargs)
