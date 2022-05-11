from rest_framework import serializers

from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantMenuSerializer(RestaurantSerializer):
    menus = serializers.SerializerMethodField()
    no_of_menus = serializers.SerializerMethodField()

    def get_menus(self, restaurant):
        return restaurant.menus.all().values("id", "name", "price")

    def get_no_of_menus(self, restaurant):
        return restaurant.menus.count()

    class Meta(RestaurantSerializer.Meta):
        fields = [
            "id",
            "name",
            "no_of_menus",
            "menus",
        ]
