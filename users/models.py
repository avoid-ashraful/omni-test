from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


from restaurants.models import Menu, Restaurant


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=255)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name


class PurchaseHistory(models.Model):
    user = models.ForeignKey(
        User, related_name="purchase_history", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu, related_name="purchase_history", on_delete=models.CASCADE
    )
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transacted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.menu}"

    def clean(self):
        if self.user.cash_balance < self.menu.price:
            raise ValidationError(
                {
                    "cash_balance": [
                        "The user does not have sufficient funds to purchase",
                    ]
                }
            )

    def save(self, *args, **kwargs):
        self.clean()

        with transaction.atomic():
            # locking rows until the end of the transaction
            user = User.objects.select_for_update().filter(id=self.user.id)
            restaurant = Restaurant.objects.select_for_update().filter(
                id=self.menu.restaurant.id
            )

            user.update(cash_balance=self.user.cash_balance - self.menu.price)
            restaurant.update(
                cash_balance=self.menu.restaurant.cash_balance + self.menu.price
            )

            self.transaction_amount = self.menu.price
            return super(PurchaseHistory, self).save(*args, **kwargs)
