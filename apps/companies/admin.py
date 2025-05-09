from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nit', 'name', 'address', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('nit', 'name', 'address', 'phone')
    ordering = ('name',)
