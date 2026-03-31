from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock_quantity', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'category__name')
    readonly_fields = ('created_at',)
    list_editable = ('price', 'stock_quantity', 'is_active')
