from dateutil import parser
from datetime import datetime

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Prefetch

from restaurants.filters import RestaurantFilter
from restaurants.models import Menu, Restaurant, RestaurantTimeSlot
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter

    def get_queryset(self):

        menu_price_query = {}
        if self.request.query_params.get("price_min"):
            menu_price_query["price__gte"] = self.request.query_params.get("price_min")
        if self.request.query_params.get("price_max"):
            menu_price_query["price__lte"] = self.request.query_params.get("price_max")

        search_restaurant_query = {}
        search_menu_query = {}
        if self.request.query_params.get("search"):
            search_restaurant_query["name__icontains"] = self.request.query_params.get(
                "search"
            )
            search_menu_query["name__icontains"] = self.request.query_params.get(
                "search"
            )

        menus = Menu.objects.filter(**menu_price_query, **search_menu_query)
        return (
            Restaurant.objects.filter(
                Q(**search_restaurant_query)
                | Q(menus__name__icontains=self.request.query_params.get("search", ""))
            )
            .prefetch_related(Prefetch("menus", queryset=menus))
            .annotate(total_menu=Count("menus", filter=Q(menus__in=menus)))
        )
