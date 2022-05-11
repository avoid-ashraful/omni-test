from django.core.management.base import BaseCommand


import json, re

from restaurants.models import Menu, Restaurant, RestaurantTimeSlot
from restaurants.utils import (
    get_concurrent_days,
    get_isoweekday,
    get_opening_closing_time_object,
)


def add_restaurants(restaurants):
    if Restaurant.objects.count():
        return 0

    restaurants_objects = [
        Restaurant(
            **{
                "name": restaurant.get("restaurantName"),
                "cash_balance": restaurant.get("cashBalance"),
            }
        )
        for restaurant in restaurants
    ]
    restaurants = Restaurant.objects.bulk_create(restaurants_objects)
    return len(restaurants)


def add_restaurant_timeslots(restaurants):
    if RestaurantTimeSlot.objects.count():
        return 0

    all_restaurant_timeslots = []
    for restaurant in restaurants:
        each_restaurant = {}
        each_restaurant["restaurant_name"] = restaurant.get("restaurantName")
        timeslots = restaurant.get("openingHours", "").replace(" ", "").split("/")

        for timeslot in timeslots:
            day, time = re.split(r"(^[^\d]+)", timeslot)[1:]
            day = day.split(",")
            opening_time, closing_time = get_opening_closing_time_object(time)

            for each_day in day:
                all_days = []
                if "-" in each_day:
                    from_day, to_day = each_day.split("-")
                    from_day_weekday = get_isoweekday(from_day)
                    to_day_weekday = get_isoweekday(to_day)

                    all_days = all_days + get_concurrent_days(
                        from_day_weekday, to_day_weekday
                    )
                else:
                    all_days.append(get_isoweekday(each_day))
                each_restaurant["all_days"] = all_days
                each_restaurant["opening_time"] = opening_time
                each_restaurant["closing_time"] = closing_time

        all_restaurant_timeslots.append(each_restaurant)

    restaurants_objects = Restaurant.objects.all()
    timeslot_objects = []
    for restaurant in all_restaurant_timeslots:
        for day in restaurant.get("all_days"):
            timeslot_objects.append(
                RestaurantTimeSlot(
                    restaurant=restaurants_objects.get(
                        name=restaurant.get("restaurant_name")
                    ),
                    day=day,
                    opening_hour=restaurant.get("opening_time"),
                    closing_hour=restaurant.get("closing_time"),
                )
            )

    restaurant_timeslot_objects = RestaurantTimeSlot.objects.bulk_create(
        timeslot_objects
    )
    return len(restaurant_timeslot_objects)


def add_menus(restaurants):
    if Menu.objects.count():
        return 0

    restaurants_objects = Restaurant.objects.all()
    menu_objects = []
    for restaurant in restaurants:
        restaurant_id = restaurants_objects.get(
            name=restaurant.get("restaurantName")
        ).id
        for menu in restaurant.get("menu"):
            menu_objects.append(
                Menu(
                    restaurant_id=restaurant_id,
                    name=menu.get("dishName"),
                    price=menu.get("price"),
                )
            )
    menus = Menu.objects.bulk_create(menu_objects)
    return len(menus)


class Command(BaseCommand):
    def handle(self, *args, **options):

        restaurant_raw_data = json.load(open("raw_data/restaurant_with_menu.json"))

        no_of_restaurants_added = add_restaurants(restaurant_raw_data)
        print(f"{no_of_restaurants_added} restaurants added!")

        no_of_restaurants_timeslot_added = add_restaurant_timeslots(restaurant_raw_data)
        print(f"{no_of_restaurants_timeslot_added} restaurant timeslots added!")

        no_of_menus_added = add_menus(restaurant_raw_data)
        print(f"{no_of_menus_added} menus added!")
