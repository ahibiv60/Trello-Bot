import time
from datetime import datetime, timedelta
from app.utils.logger import log_to_file

def is_working_hours():
    now = datetime.now()
    if now.weekday() >= 5:  # 5 і 6 – це субота або неділя
        return False
    if now.hour < 9 or (now.hour == 18 and now.minute > 30) or now.hour > 18:
        return False
    return True

def wait_until_working_hours():
    now = datetime.now()

    if is_working_hours():
        return

    log_to_file("Non-working time now. Calculating the time until work starts...")

    if now.weekday() < 5 and now.hour < 9:
        next_working_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        days_ahead = 1 if now.weekday() < 4 else (7 - now.weekday())
        next_working_time = (now + timedelta(days=days_ahead)).replace(hour=9, minute=0, second=0, microsecond=0)

    seconds_to_wait = (next_working_time - now).total_seconds()
    
    log_to_file(f"Waiting for {next_working_time.strftime('%Y-%m-%d %H:%M:%S')} ({int(seconds_to_wait)} seconds)...")
    time.sleep(seconds_to_wait)