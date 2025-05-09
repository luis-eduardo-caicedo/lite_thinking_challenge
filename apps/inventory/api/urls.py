from django.urls import path
from .views import InventoryListCreateView, InventoryDetailView, InventoryByProductView


urlpatterns = [
    path('', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
    path('by-product/<int:product_id>/', InventoryByProductView.as_view(), name='inventory-by-product'),
]
