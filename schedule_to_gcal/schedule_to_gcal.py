from facility_scheduler import get_schedule
from gcal_setup import add_time
from gcal_event import create_event
from gcal_event import get_events
from gcal_event import delete_event
from os import environ
# from dotenv import load_dotenv
# load_dotenv()

# Returns a dictionary with the start time in isoformat as the key and
# a list containing the start time as a datetime object, shift type as a string, and a boolean if the shift is canceled as the values
# Ex: '2021-06-06T19:00:00-05:00': [datetime.datetime(2021, 6, 6, 19).astimezone(pytz.timezone('America/Chicago')), 'P', False]
def get_shifts():
    shifts = get_schedule()
    return shifts


# Updates the Google Calendar by removing events that were canceled
def remove_canceled_events(shifts):
    canceled_shifts = set()
    for k, v in list(shifts.items()):
        iso_dt, dt, shift_type, canceled = k, v[0], v[1], v[2]
        if canceled:
            canceled_shifts.add(iso_dt)
            del shifts[iso_dt]

    events = get_events()
    for iso_dt, event_id in events.items():
        if iso_dt in canceled_shifts:
            delete_event(event_id)

    return shifts


# Adds the shifts to the Google Calendar
def add_event(shifts):
    events = get_events()
    # The intersection of the schedule dates and the event dates
    duplicates = shifts.keys() & events.keys()

    # Deletes the shifts that already exist on the Google Calendar from the dictionary
    for k in duplicates:
        del shifts[k]

    for k, v in shifts.items():
        start_time = k
        end_time = v[0] + add_time(12)
        summary = environ.get('SUMMARY')
        desc = v[1]
        location = environ.get('LOCATION')
        create_event(start_time, end_time, summary, desc, location)


def main():
    shifts = get_shifts()
    remove_canceled = remove_canceled_events(shifts)
    add_event(remove_canceled)


if __name__ == "__main__":
    main()
