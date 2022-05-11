from rest_framework import serializers

from restaurants.models import Restaurant, RestaurantTimeSlot


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
