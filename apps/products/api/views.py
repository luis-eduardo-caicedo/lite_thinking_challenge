from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import Product
from .serializers import ProductSerializer


class ProductListCreateView(APIView):
    """
    GET  /api/products/       → list active products
    POST /api/products/       → create product (admin only)
    """

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        code = request.data.get('code')
        if Product.objects.filter(code=code, is_active=True).exists():
            return Response({'detail': 'A product with this code already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """
    GET    /api/products/{pk}/   → retrieve product
    PUT    /api/products/{pk}/   → update product (admin only)
    DELETE /api/products/{pk}/   → logical delete (admin only)
    """

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk, is_active=True)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        product = self.get_object(pk)
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
