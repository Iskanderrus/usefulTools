import datetime
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle

# Define the scope for Google Calendar API access
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_task(name, description, time_of_day, start_date, time_zone):
    """
    Creates a series of tasks in Google Calendar based on user-defined intervals.

    :param name: Task name (string)
    :param description: Task description (string)
    :param time_of_day: Time of the task (string, format 'HH:MM')
    :param start_date: Start date of the task series (string, format 'YYYY-MM-DD')
    :param time_zone: Time zone for the events (string, e.g., 'Europe/Berlin')
    """
    # Convert date and time to a datetime object
    task_time = datetime.datetime.strptime(f"{start_date} {time_of_day}", '%Y-%m-%d %H:%M')

    # Get the number of intervals from the user
    number_of_intervals = int(input("How many occurrences are required: "))

    # Get each interval from the user
    intervals = [int(input(f"Provide interval {i + 1} (in days) for your task: ")) for i in range(number_of_intervals)]

    # Create a task occurrence for each date according to user-defined intervals
    for interval in intervals:
        # Calculate the date for each occurrence based on the interval
        task_date = task_time + datetime.timedelta(days=interval)
        event = {
            'summary': name,
            'description': description,
            'start': {
                'dateTime': task_date.isoformat(),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': (task_date + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': time_zone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # Reminder 1 day in advance
                    {'method': 'popup', 'minutes': 30},       # Reminder 30 minutes in advance
                ],
            },
        }

        # Insert the event into Google Calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Task created: {event_result.get('htmlLink')}")

# Authentication and credentials loading
creds = None
# Check if a token file exists (used for storing access and refresh tokens)
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If no valid credentials are available, prompt the user to log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        # Refresh expired credentials if a refresh token is available
        creds.refresh(Request())
    else:
        # Perform OAuth 2.0 login flow if no credentials are available
        flow = InstalledAppFlow.from_client_secrets_file(
            'sources/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for future runs
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Create the Google Calendar API service
service = build('calendar', 'v3', credentials=creds)

# Main script execution
if __name__ == "__main__":
    # Prompt the user for task details
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    time_of_day = input("Enter time of day (HH:MM): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    time_zone = input("Enter time zone (e.g., 'Europe/Berlin'): ")

    # Create the task in Google Calendar with the provided details
    create_task(name, description, time_of_day, start_date, time_zone)
