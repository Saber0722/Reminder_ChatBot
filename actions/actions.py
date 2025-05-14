from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os
from datetime import datetime
from dateutil import parser

# File to store reminders
REMINDERS_FILE = "reminders.json"

class ActionSaveReminder(Action):
    def name(self) -> Text:
        return "action_save_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get task and time from slots
        task = tracker.get_slot("task")
        time = tracker.get_slot("time")

        if not task or not time:
            dispatcher.utter_message(text="I need both a task and a time to set a reminder.")
            return []

        # Parse the time to a datetime object
        try:
            reminder_time = parser.parse(time, fuzzy=True)
        except ValueError:
            reminder_time = datetime.now()  # Fallback to current time if parsing fails

        # Load existing reminders
        reminders = []
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, "r") as f:
                reminders = json.load(f)

        # Add new reminder
        reminders.append({
            "task": task,
            "time": reminder_time.isoformat(),
            "set_time": datetime.now().isoformat()
        })

        # Save reminders to file
        with open(REMINDERS_FILE, "w") as f:
            json.dump(reminders, f, indent=2)

        return [SlotSet("task", task), SlotSet("time", time)]

class ActionViewReminders(Action):
    def name(self) -> Text:
        return "action_view_reminders"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Load reminders
        if not os.path.exists(REMINDERS_FILE):
            dispatcher.utter_message(text="You have no reminders set.")
            return []

        with open(REMINDERS_FILE, "r") as f:
            reminders = json.load(f)

        if not reminders:
            dispatcher.utter_message(text="You have no reminders set.")
            return []

        # Check for due reminders
        current_time = datetime.now()
        response = "Your reminders:\n"
        for reminder in reminders:
            task = reminder["task"]
            reminder_time = datetime.fromisoformat(reminder["time"])
            # Check if reminder is due (within 5 minutes for simplicity)
            time_diff = (current_time - reminder_time).total_seconds() / 60
            if 0 <= time_diff <= 5:
                response += f"- {task} (due now!)\n"
            else:
                response += f"- {task} at {reminder_time.strftime('%Y-%m-%d %H:%M')}\n"

        dispatcher.utter_message(text=response)
        return []