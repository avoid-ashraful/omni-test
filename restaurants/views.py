from dateutil import parser
from datetime import datetime

from rest_framework.generics import ListAPIView
from restaurants.models import Restaurant, RestaurantTimeSlot

from restaurants.serializers import RestaurantSerializer


class RestaurantListAPIView(ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        url_datetime_params = self.request.query_params.get("datetime")
        if url_datetime_params:
            datetime_object = parser.parse(url_datetime_params)
        else:
            datetime_object = datetime.now()

        restaurant_ids = RestaurantTimeSlot.objects.filter(
            opening_hour__lte=datetime_object.time(),
            closing_hour__gte=datetime_object.time(),
            day=datetime_object.isoweekday(),
        ).values_list("restaurant_id", flat=True)
        return Restaurant.objects.filter(id__in=restaurant_ids)
