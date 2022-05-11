from factory import Faker, django, SubFactory
from restaurants.tests.factories import MenuFactory
from users.models import PurchaseHistory, User


class UserFactory(django.DjangoModelFactory):
    name = Faker("word")

    class Meta:
        model = User


class PurchaseHistoryFactory(django.DjangoModelFactory):
    user = SubFactory(UserFactory)
    menu = SubFactory(MenuFactory)

    class Meta:
        model = PurchaseHistory
