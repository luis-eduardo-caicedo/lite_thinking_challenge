from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ['id', 'code', 'name', 'features', 
                  'price_amount', 'price_currency', 'company', 'is_active']
        read_only_fields = ['id', 'is_active']