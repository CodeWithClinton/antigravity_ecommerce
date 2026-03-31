from django.test import TestCase
from .models import Category
from products.models import Product
from .serializers import CategorySerializer
from decimal import Decimal

class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        Product.objects.create(
            title='Phone',
            price=Decimal('500.00'),
            category=self.category
        )
        Product.objects.create(
            title='Laptop',
            price=Decimal('1000.00'),
            category=self.category
        )

    def test_category_serializer_total_products(self):
        serializer = CategorySerializer(self.category)
        self.assertEqual(serializer.data['total_products'], 2)
        self.assertIn('image', serializer.data)
