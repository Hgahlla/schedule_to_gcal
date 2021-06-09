from facility_scheduler import get_schedule
from gcal_setup import convert_str_to_local_datetime
from gcal_setup import add_time
from gcal_event import create_event
import secret


def get_shift_dates():
    #shift_dates = ['2021-06-07', '2021-06-08', '2021-06-09', '2021-06-14', '2021-06-16']
    shift_dates = get_schedule()
    return shift_dates


def add_event():
    shifts = get_shift_dates()

    for date in shifts:
        start_time = convert_str_to_local_datetime(date) + add_time(19)
        end_time = start_time + add_time(12)
        summary = secret.summary
        desc = "P"
        location = secret.location

        create_event(start_time, end_time, summary, desc, location)


def main():
    get_schedule()
    add_event()


if __name__ == "__main__":
    main()
