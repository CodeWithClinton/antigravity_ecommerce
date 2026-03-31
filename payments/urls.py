from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate-payment'),
    path('verify/', views.verify_payment, name='verify-payment'),
]
