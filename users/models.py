from django.db import models
from django.contrib.auth.models import AbstractUser

from restaurants.models import Menu


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=255)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []


class PurchaseHistory(models.Model):
    user = models.ForeignKey(
        User, related_name="purchase_history", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu, related_name="purchase_history", on_delete=models.CASCADE
    )
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transacted_at = models.DateTimeField(auto_now_add=True)
