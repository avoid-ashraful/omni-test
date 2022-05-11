import pytest

from datetime import datetime, timedelta
from factory import create_batch, fuzzy

from django.urls import reverse
from restaurants.models import Restaurant, RestaurantTimeSlot
from restaurants.tests.factories import (
    MenuFactory,
    RestaurantFactory,
    RestaurantTimeSlotFactory,
)
from rest_framework import status


class Base:
    @pytest.fixture
    def restaurant(self):
        return RestaurantFactory(name=fuzzy.FuzzyText().fuzz())

    @pytest.fixture
    def restaurant_timeslot(self, restaurant):
        return RestaurantTimeSlotFactory(
            restaurant=restaurant,
            day=datetime.now().isoweekday(),
            opening_hour=datetime.now().time(),
            closing_hour=(datetime.now() + timedelta(hours=2)).time(),
        )

    @pytest.fixture
    def url(self):
        return reverse(
            "api:restaurants:list",
        )


class TestRestaurantViews(Base):
    def test_restaurant_list_api(self, client, url, restaurant_timeslot):
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1

    def test_restaurant_list_api_with_datetime_params(
        self, client, url, restaurant_timeslot
    ):
        response = client.get(
            url,
            kwargs={datetime: datetime.now()},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1

    def test_restaurant_list_api_with_outranged_datetime_params(
        self, client, url, restaurant_timeslot
    ):
        response = client.get(
            f"{url}?datetime={(datetime.now() + timedelta(hours=3)).isoformat()}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0


class TestRestaurantMenuListViews(Base):
    @pytest.fixture
    def url(self):
        return reverse(
            "api:restaurants:list-menu",
        )

    def test_restaurant_top_list_api(self, client, url, restaurant):
        menus = MenuFactory.create_batch(size=10, restaurant=restaurant)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("results", [{}])[0].get("no_of_menus")

    def test_restaurant_top_list_api_with_params_less(self, client, url, restaurant):
        menus = MenuFactory.create_batch(size=10, restaurant=restaurant)
        response = client.get(f"{url}?eq=less&no_of_dish=11")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1
        assert response.data.get("results", [{}])[0].get("no_of_menus") == 10

    def test_restaurant_top_list_api_with_params_more(self, client, url, restaurant):
        menus = MenuFactory.create_batch(size=10, restaurant=restaurant)
        response = client.get(f"{url}?eq=more&no_of_dish=9")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1
        assert response.data.get("results", [{}])[0].get("no_of_menus") == 10


class TestRestaurantMenuSearchListViews(Base):
    @pytest.fixture
    def url(self):
        return reverse(
            "api:restaurants:list-menu",
        )

    def test_restaurant_menu_search_api_by_restaurant(self, client, url, restaurant):
        response = client.get(f"{url}?search={restaurant.name[:3]}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1

    def test_restaurant_menu_search_api_by_restaurant_error(
        self, client, url, restaurant
    ):
        response = client.get(f"{url}?search={fuzzy.FuzzyText().fuzz()}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0

    def test_restaurant_menu_search_api_by_menu(self, client, url):
        menu = MenuFactory(name=fuzzy.FuzzyText().fuzz())

        response = client.get(f"{url}?search={menu.name[:3]}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1

    def test_restaurant_menu_search_api_by_menu_error(self, client, url, restaurant):
        menu = MenuFactory(name=fuzzy.FuzzyText().fuzz())

        response = client.get(f"{url}?search={fuzzy.FuzzyText().fuzz()}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0
