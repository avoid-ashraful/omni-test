import datetime
from restaurants.models import RestaurantTimeSlot


def get_isoweekday(day):
    for choice in RestaurantTimeSlot.DAY_CHOICES:
        if day in choice[1]:
            return choice[0]


def get_concurrent_days(start, end):
    start, end = int(start), int(end)
    if start < end:
        return list(range(start, end + 1))
    return list(range(start, 8)) + list(range(1, end + 1))


def get_time_object(time_str):
    if ":" in time_str:
        return datetime.datetime.strptime(time_str, "%I:%M%p").time()
    return datetime.datetime.strptime(time_str, "%I%p").time()


def get_opening_closing_time_object(time_str):
    start_time, end_time = time_str.split("-")
    return get_time_object(start_time), get_time_object(end_time)
