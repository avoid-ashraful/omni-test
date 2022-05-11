from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from users.models import PurchaseHistory
from rest_framework.permissions import AllowAny

from users.serializers import PurchaseHistorySerializer


class PurchaseHistoryListAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PurchaseHistorySerializer
    queryset = PurchaseHistory.objects.all()
