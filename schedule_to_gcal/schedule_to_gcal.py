from facility_scheduler import get_schedule
from gcal_setup import convert_str_to_local_datetime
from gcal_setup import add_time
from gcal_event import create_event
import secret

def add_event():
    shifts = get_schedule()

    for date, shift_type in shifts:
        start_time = convert_str_to_local_datetime(date) + add_time(19)
        end_time = start_time + add_time(12)
        summary = secret.summary
        desc = shift_type
        location = secret.location

        create_event(start_time, end_time, summary, desc, location)


def main():
    add_event()

if __name__ == "__main__":
    main()
