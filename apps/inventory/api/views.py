from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import Inventory
from .serializers import InventorySerializer


class InventoryListCreateView(APIView):
    """
    GET  /api/inventory/       → list all active inventory items
    POST /api/inventory/       → create inventory (admin only)
    """
    def get(self, request):
        inventory = Inventory.objects.filter(is_active=True)
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        product_id = request.data.get('product')
        if Inventory.objects.filter(product_id=product_id, is_active=True).exists():
            return Response({'detail': 'This product is already in inventory.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryDetailView(APIView):
    """
    GET    /api/inventory/{id}/   → retrieve one item
    PUT    /api/inventory/{id}/   → update (admin only)
    DELETE /api/inventory/{id}/   → logical delete (admin only)
    """
    def get_object(self, pk):
        return get_object_or_404(Inventory, pk=pk, is_active=True)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = InventorySerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        item = self.get_object(pk)
        serializer = InventorySerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        item = self.get_object(pk)
        item.is_active = False
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InventoryByProductView(APIView):
    """
    GET /api/inventory/by-product/{product_id}/ → Obtener inventario por producto
    """

    def get(self, request, product_id):
        try:
            inventory = Inventory.objects.get(product_id=product_id, is_active=True)
        except Inventory.DoesNotExist:
            return Response({'detail': 'No inventory found for this product.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventorySerializer(inventory)
        return Response(serializer.data)
