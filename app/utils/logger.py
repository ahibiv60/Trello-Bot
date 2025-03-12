import os
from datetime import datetime

def log_to_console(message):
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"{current_time} {message}")

def log_to_file(message, filename="logs/log.txt"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as log_file:
        log_file.write(f"{current_time} {message}\n")