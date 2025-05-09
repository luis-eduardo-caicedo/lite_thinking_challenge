from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import Company
from .serializers import CompanySerializer


class CompanyListCreateView(APIView):
    """
    GET  /api/companies/    → list all active companies (public)
    POST /api/companies/    → create a new company (admin only)
    """
    def get(self, request):
        companies = Company.objects.filter(is_active=True)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CompanyDetailView(APIView):
    """ 
    GET    /api/companies/{nit}/  → retrieve one company (public)
    PUT    /api/companies/{nit}/  → update company (admin only)
    DELETE /api/companies/{nit}/  → logical delete (admin only)
    """
    def get_object(self, nit):
        return get_object_or_404(Company, nit=nit, is_active=True)

    def get(self, request, nit):
        company = self.get_object(nit)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, nit):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        company = self.get_object(nit)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, nit):
        user = request.user
        if not user.is_authenticated or not user.is_admin:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        company = self.get_object(nit)
        company.is_active = False
        company.save()
        return Response(status=status.HTTP_204_NO_CONTENT)