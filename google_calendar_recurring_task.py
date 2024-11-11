import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Setting Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'sources/credentials.json'

# Load credentials and initialize the Google Calendar API service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)


def create_task(name, description, time_of_day, start_date, time_zone):
    """
    Creates a series of tasks in Google Calendar based on user-defined intervals.

    :param name: Task name (str)
    :param description: Task description (str)
    :param time_of_day: Time of day for the task in 'HH:MM' format (str)
    :param start_date: Start date of the task in 'YYYY-MM-DD' format (str)
    :param time_zone: Time zone for the events (str), e.g., 'America/New_York'
    """
    # Parse start_date and time_of_day into a datetime object
    task_time = datetime.datetime.strptime(f"{start_date} {time_of_day}", '%Y-%m-%d %H:%M')

    # Prompt user for the number of intervals (task occurrences) they want
    number_of_intervals = int(input("How many occurrences are required: "))

    # Collect intervals from the user, in days, for each occurrence
    intervals = []
    for i in range(number_of_intervals):
        interval = int(input(f"Provide interval {i + 1} (in days) for your task: "))
        intervals.append(interval)

    # Create and insert an event into Google Calendar for each interval
    for interval in intervals:
        task_date = task_time + datetime.timedelta(days=interval)
        event = {
            'summary': name,
            'description': description,
            'start': {
                'dateTime': task_date.isoformat(),
                'timeZone': time_zone,  # Set to specified time zone
            },
            'end': {
                'dateTime': (task_date + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': time_zone,
            },
            'visibility': 'default',  # Make the event visible to the user
            'guestsCanSeeOtherGuests': True,  # Allow guests to see each other
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # Reminder 1 day in advance
                    {'method': 'popup', 'minutes': 30},  # Reminder 30 minutes in advance
                ],
            },
        }

        # Insert the event into the Google Calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Task created: {event_result.get('htmlLink')}")


if __name__ == "__main__":
    # Collect user input for task details
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    time_of_day = input("Enter time of day (HH:MM): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    time_zone = input("Enter time zone (e.g., 'America/New_York'): ")

    # Call create_task with user-provided input
    create_task(name, description, time_of_day, start_date, time_zone)
