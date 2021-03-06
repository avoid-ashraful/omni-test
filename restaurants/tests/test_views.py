import pytest

from datetime import datetime, timedelta
from factory import fuzzy

from django.urls import reverse
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
        MenuFactory.create_batch(size=10, restaurant=restaurant)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("results", [{}])[0].get("total_menu")

    def test_restaurant_top_list_api_with_params_total_menu_with_range(
        self, client, url, restaurant
    ):
        MenuFactory.create_batch(size=10, restaurant=restaurant)
        response = client.get(f"{url}?total_menu_min=9&total_menu_max=11")

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1
        assert response.data.get("results", [{}])[0].get("total_menu") == 10

    def test_restaurant_top_list_api_with_params_total_menu_with_out_range(
        self, client, url, restaurant
    ):
        MenuFactory.create_batch(size=10, restaurant=restaurant)
        response = client.get(f"{url}?total_menu_min=11&total_menu_max=12")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0
        assert not response.data.get("results")

    def test_restaurant_top_list_api_with_params_menu_price_with_range(
        self, client, url, restaurant
    ):
        menus = MenuFactory.create_batch(size=10, restaurant=restaurant)
        menus[0].price = 100
        menus[0].save()

        response = client.get(f"{url}?price_min=99&price_max=101")

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 1
        assert response.data.get("results", [{}])[0].get("total_menu") == 1


class TestRestaurantMenuSearchListViews(TestRestaurantMenuListViews):
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
        MenuFactory(name=fuzzy.FuzzyText().fuzz())

        response = client.get(f"{url}?search={fuzzy.FuzzyText().fuzz()}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0
