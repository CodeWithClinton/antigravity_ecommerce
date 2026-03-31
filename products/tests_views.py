from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product
from categories.models import Category
from decimal import Decimal

class ProductViewsTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.p1 = Product.objects.create(
            title='Featured Product',
            price=Decimal('10.00'),
            is_featured=True,
            category=self.category
        )
        self.p2 = Product.objects.create(
            title='Regular Product',
            price=Decimal('20.00'),
            is_featured=False,
            category=self.category
        )

    def test_featured_products(self):
        url = reverse('featured-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Featured Product')

    def test_latest_products(self):
        url = reverse('latest-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Latest should be p2 then p1 (since p2 was created after p1)
        self.assertEqual(response.data[0]['title'], 'Regular Product')
