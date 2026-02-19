import os
from datetime import datetime

def _build_message(level, component, message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{current_time} {level} {component} | {message}"


def log_to_console(message, level="INFO", component="app"):
    print(_build_message(level, component, message))


def log_to_file(message, filename="logs/log.txt", level="INFO", component="app"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a", encoding="utf-8") as log_file:
        log_file.write(f"{_build_message(level, component, message)}\n")
