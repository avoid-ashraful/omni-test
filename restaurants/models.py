from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class RestaurantTimeSlot(models.Model):
    DAY_CHOICES = [
        (1, "Mon"),
        (2, "Tues"),
        (3, "Weds"),
        (4, "Thurs"),
        (5, "Fri"),
        (6, "Sat"),
        (7, "Sun"),
    ]

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="time_slots"
    )
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()

    class Meta:
        unique_together = (
            "restaurant",
            "day",
            "opening_hour",
            "closing_hour",
        )


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
