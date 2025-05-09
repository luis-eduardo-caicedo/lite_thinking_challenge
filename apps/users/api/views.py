from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer
from ..models import User
from .serializers import UserSerializer
from ..permissions import IsAdministrator


class UserListCreateView(APIView):
    """
    GET  /api/auth/users/    → list all active users (admin only)
    POST /api/auth/users/    → create a new user (admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        # Hash password before creating
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    """
    GET    /api/auth/users/{id}/   → retrieve one user (admin only)
    PUT    /api/auth/users/{id}/   → update user (admin only)
    DELETE /api/auth/users/{id}/   → logical delete (admin only)
    """
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk, is_active=True)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = UserSerializer(user, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        return Response(UserSerializer(updated).data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/token/  
    Request body: { "email": "...", "password": "..." }
    Response: {
      "refresh": "...",
      "access": "...",
      "is_admin": true|false
    }
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    POST /api/auth/token/refresh/  
    Request body: { "refresh": "..." }
    Response: { "access": "..." }
    """
    # Usa el serializer por defecto de SimpleJWT
    pass