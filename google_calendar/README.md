
# Google Calendar Recurring Task Creator

This Python script allows users to create recurring tasks on Google Calendar. The tasks can be scheduled based on user-defined intervals or the default intervals (3, 7, 14, 21, 35 days). Users can also choose the color of the event from a set of predefined options.

## Features
- **Create recurring tasks**: Schedule tasks at specific intervals (either custom or default).
- **Auto-detect local timezone**: The script uses the user's local timezone for the events.
- **Customizable event colors**: Choose from 11 predefined color options for the calendar event.
- **OAuth 2.0 authentication**: The script uses OAuth to authenticate and create events in the user's Google Calendar.

## Requirements

- **Python 3.6+** (Tested on Python 3.12)
- **Google API Client Library**: For Google Calendar API access.
- **`google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`**: Libraries for Google OAuth2.0 authentication and interacting with Google APIs.

### Install the required dependencies:
```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Setup

1. **Enable Google Calendar API**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or use an existing project.
   - Enable the **Google Calendar API** for the project.
   - Create **OAuth 2.0 credentials** and download the `credentials.json` file.

2. **Download the script**:
   - Clone or download the repository containing this script.
   - Place the `credentials.json` file you downloaded from Google in the `sources/` directory.

3. **Token Storage**:
   - The script will create a `token.pickle` file after the first run to store the credentials for future executions. This avoids the need for re-authentication each time.

## Usage

### Running the Script:

Run the script by executing the following command:

```bash
python google_calendar_recurring_task.py
```

### Input Prompts:
- **Task Name**: Enter the name of the task.
- **Task Description**: Provide a description for the task.
- **Time of Day**: Specify the time of day (in `HH:MM` format).
- **Start Date**: The script will use the current date by default, but you can specify a start date if needed.
- **Intervals**: You can choose to use the default intervals (3, 7, 14, 21, 35 days) or specify custom intervals.
- **Event Color**: Select from 11 color options to customize the event's color in your Google Calendar.

### Default Intervals:
If you choose to use the default intervals, the script will automatically create tasks with the following intervals:
- 3 days
- 7 days
- 14 days
- 21 days
- 35 days

If you opt to use custom intervals, you will be prompted to enter the number of occurrences and the intervals (in days).

### Example:
```bash
Enter task name: Test Task
Enter task description: Test task description
Enter time of day (HH:MM): 14:00
Using current date as start date: 2024-11-11
Do you want to use the default intervals (3, 7, 14, 21, 35 days)? (y/n): y
Available colors for the event:
1: Lavender
2: Sage
3: Grape
4: Flamingo
5: Banana
6: Tangerine
7: Peacock
8: Graphite
9: Blueberry
10: Basil
11: Tomato
Enter the color ID for the event (1-11): 1
Task occurrence 1 created: https://www.google.com/calendar/event?eid=xyz123
Task occurrence 2 created: https://www.google.com/calendar/event?eid=abc456
```

### Authentication:
On the first run, the script will prompt you to log in to your Google account and authorize the script to manage your calendar. The authorization token will be stored in the `token.pickle` file for future use.

## Notes:
- This script requires an active internet connection for authenticating and interacting with the Google Calendar API.
- Make sure your `credentials.json` file is correctly placed in the `sources/` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this repository, make improvements, and submit a pull request. Issues and feature requests are welcome!
