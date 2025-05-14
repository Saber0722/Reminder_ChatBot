import schedule
import time
import json
from datetime import datetime
import os

REMINDERS_FILE = "reminders.json"

def check_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return
    with open(REMINDERS_FILE, "r") as f:
        reminders = json.load(f)
    current_time = datetime.now()
    for reminder in reminders:
        task = reminder["task"]
        reminder_time = datetime.fromisoformat(reminder["time"])
        if current_time >= reminder_time and (current_time - reminder_time).total_seconds() <= 300:
            print(f"Reminder: {task} is due now!")  # Replace with notification logic

schedule.every(1).minutes.do(check_reminders)

while True:
    schedule.run_pending()
    time.sleep(60)