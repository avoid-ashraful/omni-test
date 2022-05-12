from rest_framework import serializers

from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantMenuSerializer(RestaurantSerializer):
    menus = serializers.SerializerMethodField()
    total_menu = serializers.SerializerMethodField()

    def get_menus(self, restaurant):
        return restaurant.menus.values("id", "name", "price")

    def get_total_menu(self, restaurant):
        return restaurant.total_menu

    class Meta(RestaurantSerializer.Meta):
        fields = [
            "id",
            "name",
            "total_menu",
            "menus",
        ]
