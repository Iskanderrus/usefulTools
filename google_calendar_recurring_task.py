import datetime
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import zoneinfo

# Define the scope for Google Calendar API access
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Default intervals and color options
DEFAULT_INTERVALS = [3, 7, 14, 21, 35]
COLOR_OPTIONS = {
    "1": "Lavender",
    "2": "Sage",
    "3": "Grape",
    "4": "Flamingo",
    "5": "Banana",
    "6": "Tangerine",
    "7": "Peacock",
    "8": "Graphite",
    "9": "Blueberry",
    "10": "Basil",
    "11": "Tomato"
}

def create_task(name, description, time_of_day, start_date, time_zone, intervals, color_id):
    """
    Creates a series of tasks in Google Calendar based on specified intervals.

    :param name: Task name (string)
    :param description: Task description (string)
    :param time_of_day: Time of the task (string, format 'HH:MM')
    :param start_date: Start date of the task series (string, format 'YYYY-MM-DD')
    :param time_zone: Time zone for the events (string, e.g., 'Europe/Berlin')
    :param intervals: List of intervals in days for each task occurrence
    :param color_id: Color ID for the event (string, 1-11)
    """
    # Convert date and time to a datetime object
    task_time = datetime.datetime.strptime(f"{start_date} {time_of_day}", '%Y-%m-%d %H:%M')

    for i, interval in enumerate(intervals):
        # Calculate the date for each occurrence based on the interval
        task_date = task_time + datetime.timedelta(days=interval)
        event = {
            'summary': f"{name} - Occurrence {i + 1}",
            'description': description,
            'start': {
                'dateTime': task_date.isoformat(),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': (task_date + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': time_zone,
            },
            'colorId': color_id,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        # Insert the event into Google Calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Task occurrence {i + 1} created: {event_result.get('htmlLink')}")

# Authentication and credentials loading
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'sources/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

if __name__ == "__main__":
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    time_of_day = input("Enter time of day (HH:MM): ")

    # Use the current date as the start date
    start_date = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"Using current date as start date: {start_date}")

    # Get the user's local timezone
    time_zone = datetime.datetime.now().astimezone().tzinfo
    if not time_zone:
        raise RuntimeError("Could not determine the local timezone.")
    time_zone = str(time_zone)
    print(f"Using detected timezone: {time_zone}")

    # Ask if the user wants to use default intervals or custom ones
    use_default_intervals = input("Do you want to use the default intervals (3, 7, 14, 21, 35 days)? (y/n): ").strip().lower()
    if use_default_intervals == 'y':
        intervals = DEFAULT_INTERVALS
    else:
        number_of_intervals = int(input("How many occurrences are required: "))
        intervals = [int(input(f"Provide interval {i + 1} (in days) for your task: ")) for i in range(number_of_intervals)]

    # Display color options and get the user's choice
    print("\nAvailable colors for the event:")
    for code, color in COLOR_OPTIONS.items():
        print(f"{code}: {color}")
    color_id = input("Enter the color ID for the event (1-11): ").strip()
    if color_id not in COLOR_OPTIONS:
        print("Invalid color ID, defaulting to 1 (Lavender).")
        color_id = "1"

    # Create the task in Google Calendar with the provided details
    create_task(name, description, time_of_day, start_date, time_zone, intervals, color_id)
