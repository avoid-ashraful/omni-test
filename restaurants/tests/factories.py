
from factory import Faker, django, SubFactory, fuzzy
from restaurants.models import Menu, Restaurant, RestaurantTimeSlot


class RestaurantFactory(django.DjangoModelFactory):
    name = Faker("word")
    class Meta:
        model = Restaurant



class RestaurantTimeSlotFactory(django.DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    day = fuzzy.FuzzyChoice(choices=[choice[0] for choice in RestaurantTimeSlot.DAY_CHOICES])
    opening_hour = Faker("time")
    closing_hour = Faker("time")

    class Meta:
        model = RestaurantTimeSlot


class MenuFactory(django.DjangoModelFactory):
    restaurant = SubFactory(RestaurantFactory)
    name = Faker("word")

    class Meta:
        model = Menu
