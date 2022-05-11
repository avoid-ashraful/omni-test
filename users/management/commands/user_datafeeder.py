from django.core.management.base import BaseCommand

from datetime import datetime
import json

from restaurants.models import Restaurant
from users.models import PurchaseHistory, User


def add_users(data):
    if User.objects.count():
        return 0

    user_objects = [
        User(
            **{
                "id": user.get("id"),
                "name": user.get("name"),
                "cash_balance": user.get("cashBalance"),
            }
        )
        for user in data
    ]
    users = User.objects.bulk_create(user_objects)
    return len(users)


def add_user_purchase_history(data):
    if PurchaseHistory.objects.count():
        return 0

    all_restaurants = Restaurant.objects.all()
    purchase_entry = []

    for user in data:
        user_id = user.get("id")
        for each_purchase in user.get("purchaseHistory", []):
            restaurant = all_restaurants.get(name=each_purchase.get("restaurantName"))
            purchase_entry.append(
                PurchaseHistory(
                    user_id=user_id,
                    menu=restaurant.menus.get(name=each_purchase.get("dishName")),
                    transaction_amount=each_purchase.get("transactionAmount"),
                    transacted_at=datetime.strptime(
                        each_purchase.get("transactionDate"), "%m/%d/%Y %I:%M %p"
                    ),
                )
            )

    purchases = PurchaseHistory.objects.bulk_create(purchase_entry)
    return len(purchases)


class Command(BaseCommand):
    def handle(self, *args, **options):

        users_raw_data = json.load(open("raw_data/users_with_purchase_history.json"))

        no_of_users_added = add_users(users_raw_data)
        print(f"{no_of_users_added} users added!")

        no_of_purchase_entry_added = add_user_purchase_history(users_raw_data)
        print(f"{no_of_purchase_entry_added} purchase entry added!")
