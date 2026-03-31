from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart, name='get-cart'),
    path('add/', views.add_to_cart, name='add-to-cart'),
    path('update/', views.update_cart_item, name='update-cart-item'),
    path('remove/', views.remove_from_cart, name='remove-from-cart'),
]
