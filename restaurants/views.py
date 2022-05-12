from dateutil import parser
from datetime import datetime

from rest_framework.generics import ListAPIView
from restaurants.models import Restaurant, RestaurantTimeSlot

from django.db.models import Count, Q

from restaurants.serializers import RestaurantMenuSerializer, RestaurantSerializer


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


class RestaurantMenuListAPIView(ListAPIView):
    serializer_class = RestaurantMenuSerializer

    def get_queryset(self):
        queryset = Restaurant.objects.prefetch_related("menus").all().order_by("-name")

        search = self.request.query_params.get("search", "")
        if search:
            return queryset.filter(
                Q(name__icontains=search) | Q(menus__name__icontains=search)
            )

        equation = self.request.query_params.get("eq")
        no_of_dish = self.request.query_params.get("no_of_dish")

        if not (equation and no_of_dish):
            return queryset
        query_params = {}
        if equation == "more":
            query_params["m__gt"] = int(no_of_dish)
        else:
            query_params["m__lt"] = int(no_of_dish)
        return queryset.annotate(m=Count("menus")).filter(**query_params)
