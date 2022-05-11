from django.urls import path

from restaurants.views import RestaurantListAPIView

app_name = "restaurants"


urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="list"),
]
