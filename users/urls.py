from django.urls import path

from users.views import PurchaseHistoryListAPIView


app_name = "users"


urlpatterns = [
    path("orders/", PurchaseHistoryListAPIView.as_view(), name="order-create"),
]
