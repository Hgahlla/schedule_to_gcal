from gcal_setup import create_service
import secret
import datetime
import pytz

CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
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

    # Call the Calendar API: Creates an event.
    response = service.events().insert(calendarId=calendar_id, body=event_request_body).execute()

    print("Event Created in", response['organizer']['displayName'])
    print("Title:", response['summary'])
    print("Start Time:", response['start']['dateTime'])
    print("End Time:", response['end']['dateTime'], "\n")


# Returns events on the specified calendar
def get_events():
    page_token = None
    events = {}
    while True:
        # Call the Calendar API: Returns events on the specified calendar.
        event_list = service.events().list(calendarId=calendar_id, pageToken=page_token, orderBy='startTime', singleEvents=True).execute()
        for event in event_list['items']:
            start_time = event['start']['dateTime']
            events[start_time] = event['id']

        page_token = event_list.get('nextPageToken')
        if not page_token:
            break

    return events


# Deletes an event
def delete_event(event_id):
    # Call the Calendar API: Deletes an event.
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    print("The Event (" + str(event_id) + ") Was Successfully Deleted")
