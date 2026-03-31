from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('featured/', views.featured_products, name='featured-products'),
    path('latest/', views.latest_products, name='latest-products'),
    path('search/', views.product_search, name='product-search'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
]
