import pytest
from django.urls import reverse
from restaurants.tests.factories import (
    MenuFactory,
    RestaurantFactory,
)
from rest_framework import status
from users.tests.factories import UserFactory


class Base:
    @pytest.fixture
    def user(self):
        return UserFactory(cash_balance=500)

    @pytest.fixture
    def restaurant(self):
        return RestaurantFactory(cash_balance=2000)

    @pytest.fixture
    def menu(self, restaurant):
        return MenuFactory(price=10, restaurant=restaurant)

    @pytest.fixture
    def url(self):
        return reverse(
            "api:users:order-create",
        )


class TestPurchaseHistoryrCreateViews(Base):
    def test_purchase_history_creation_api(self, client, url, user, menu, restaurant):

        assert user.cash_balance == 500
        assert menu.price == 10
        assert restaurant.cash_balance == 2000

        data = {"user": user.id, "menu": menu.id}

        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        user.refresh_from_db()
        menu.refresh_from_db()
        restaurant.refresh_from_db()

        assert user.cash_balance == 500 - menu.price
        assert menu.price == 10
        assert restaurant.cash_balance == 2000 + menu.price

    def test_purchase_history_creation_api_with_insuficient_funds(
        self, client, url, user, menu, restaurant
    ):
        user.cash_balance = 5
        user.save()

        data = {"user": user.id, "menu": menu.id}

        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert user.cash_balance == 5
        assert menu.price == 10
        assert restaurant.cash_balance == 2000
