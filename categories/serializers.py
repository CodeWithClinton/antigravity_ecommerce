from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    total_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'is_active', 'total_products')

    def get_total_products(self, obj):
        return obj.products.count()
