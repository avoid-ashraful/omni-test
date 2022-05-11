from rest_framework import serializers

from restaurants.models import Restaurant, RestaurantTimeSlot


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantMenuSerializer(RestaurantSerializer):
    menu = serializers.SerializerMethodField()

    def get_menu(self, restaurant):
        return restaurant.menus.all().values("id", "name", "price")

    class Meta(RestaurantSerializer.Meta):
        fields = ["id", "name", "menu"]
