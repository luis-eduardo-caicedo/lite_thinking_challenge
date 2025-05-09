from django.urls import path
from .views import CompanyListCreateView, CompanyDetailView

urlpatterns = [
    path('',         CompanyListCreateView.as_view(), name='company-list-create'),
    path('<str:nit>/', CompanyDetailView.as_view(),   name='company-detail'),
]