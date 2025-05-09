from rest_framework import serializers
from ..models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = ['nit', 'name', 'address', 'phone', 'is_active']
        read_only_fields = ['is_active']
