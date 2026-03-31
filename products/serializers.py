from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'stock_quantity', 'category', 'category_name', 'category_slug', 'image', 'is_active', 'created_at')
