from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'is_active')
    list_filter = ('is_active', 'product__company')
    search_fields = ('product__name', 'product__code')
    ordering = ('-quantity',)