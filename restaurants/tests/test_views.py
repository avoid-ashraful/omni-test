import pytest

from datetime import datetime, timedelta

from django.urls import reverse
from restaurants.models import Restaurant, RestaurantTimeSlot
from restaurants.tests.factories import RestaurantFactory, RestaurantTimeSlotFactory
from rest_framework import status


class Base:
    @pytest.fixture
    def restaurant(self):
        return RestaurantFactory()

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
        print(
            restaurant_timeslot.day,
            restaurant_timeslot.opening_hour,
            restaurant_timeslot.closing_hour,
        )
        print(datetime.now() + timedelta(days=4))
        response = client.get(
            f"{url}?datetime={(datetime.now() + timedelta(hours=3)).isoformat()}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 0
