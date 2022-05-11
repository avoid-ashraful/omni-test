from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers

from users.models import PurchaseHistory


class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ["user", "menu"]

    def create(self, validated_data):

        try:
            return super().create(validated_data)
        except ValidationError as core_excp:
            raise serializers.ValidationError(core_excp)
