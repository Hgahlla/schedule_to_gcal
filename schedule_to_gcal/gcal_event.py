from gcal_setup import Create_Service
from pprint import pprint
import secret
import datetime
import pytz

CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
calendar_id = secret.calendar_id


# Create an event
def create_event(start_time, end_time, summary, desc, location):
    event_request_body = {
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Chicago'
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Chicago'
        },
        'summary': summary,
        'description': desc,
        'location': location,
    }

    # Call the Calendar API
    response = service.events().insert(calendarId=calendar_id, body=event_request_body).execute()
    pprint(response)

# Checks if an event at a given start time already exists and removes it from the dictionary
def check_event_exists(shifts):
    page_token = None
    event_times = set()
    while True:
        # Call the Calendar API
        events = service.events().list(calendarId=calendar_id, pageToken=page_token, orderBy='startTime', singleEvents=True).execute()
        for event in events['items']:
            event_times.add(event['start']['dateTime'])

        page_token = events.get('nextPageToken')
        if not page_token:
            break

    # The intersection of the schedule dates and the event dates
    duplicates = shifts.keys() & event_times

    # Deletes the events that already exist on the calendar from the dictionary
    for k in duplicates:
        del shifts[k]

    return shifts

    # # The intersection of the schedule dates and the event dates
    # print(list(set(start_times) & set(event_times)))
    #
    # # Symmetric Difference, the equivalent of the union of both sets minus the intersection of both sets
    # print(list(set(start_times) ^ set(event_times)))