from django.urls import path

from restaurants.views import RestaurantListAPIView, RestaurantMenuListAPIView

app_name = "restaurants"


urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="list"),
    path("menus/", RestaurantMenuListAPIView.as_view(), name="list-menu"),
]
