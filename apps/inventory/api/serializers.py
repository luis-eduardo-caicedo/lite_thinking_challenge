from rest_framework import serializers
from ..models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'quantity', 'is_active']
        read_only_fields = ['id', 'is_active']