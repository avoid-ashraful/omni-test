from django_filters import FilterSet, RangeFilter, CharFilter


class RestaurantFilter(FilterSet):
    def filter_price(queryset, name, value):
        return queryset

    def search_by_name(queryset, name, value):
        return queryset

    total_menu = RangeFilter(field_name="total_menu")
    price = RangeFilter(method=filter_price)

    search = CharFilter(method=search_by_name)
