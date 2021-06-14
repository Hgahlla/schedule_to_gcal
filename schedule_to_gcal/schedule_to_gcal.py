from facility_scheduler import get_schedule
from gcal_setup import add_time
from gcal_event import create_event
from gcal_event import check_event_exists
import secret
import datetime
import pytz


def get_shifts():
    shifts = get_schedule()
    return shifts


def add_event(shifts):
    shifts = check_event_exists(shifts)

    for k, v in shifts.items():
        start_time = k
        end_time = v[0] + add_time(12)
        summary = secret.summary
        desc = v[1]
        location = secret.location

        create_event(start_time, end_time, summary, desc, location)


if __name__ == "__main__":
    shifts = get_shifts()
    add_event(shifts)
