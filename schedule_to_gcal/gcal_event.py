from gcal_setup import Create_Service
from pprint import pprint
import secret

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
            'dateTime': start_time.isoformat(),
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

    response = service.events().insert(calendarId=calendar_id, body=event_request_body).execute()
    pprint(response)
