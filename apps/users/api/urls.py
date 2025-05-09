from django.urls import path
from .views import UserListCreateView, UserDetailView, CustomTokenObtainPairView, CustomTokenRefreshView, MeView

urlpatterns = [
    path('',        UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(),   name='user-detail'),
    path('me/', MeView.as_view(), name='user-me'),
    path('token/',        CustomTokenObtainPairView.as_view(),   name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]