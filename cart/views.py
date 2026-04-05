from rest_framework.decorators import api_view, permission_classes
from django_api_readme.decorators import api_doc
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import (
    CartSerializer, AddCartInputSerializer, 
    UpdateCartInputSerializer, RemoveCartInputSerializer
)
from products.models import Product

@api_doc(None, CartSerializer, summary="Get Cart", description="Retrieve the authenticated user's cart.")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_doc(AddCartInputSerializer, CartSerializer, summary="Add to Cart", description="Add a product to the user's cart.")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    product_id = request.data.get('product_id')
    try:
        quantity = int(request.data.get('quantity', 1))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
    
    if quantity < 1:
        return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found or inactive'}, status=status.HTTP_404_NOT_FOUND)
        
    # Check if item already in cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        new_quantity = cart_item.quantity + quantity
    else:
        new_quantity = quantity
        
    if new_quantity > product.stock_quantity:
        return Response(
            {'error': f'Cannot add item. Only {product.stock_quantity} in stock.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    cart_item.quantity = new_quantity
    cart_item.save()
    
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_doc(UpdateCartInputSerializer, CartSerializer, summary="Update Cart Item", description="Update the quantity of an item in the cart.")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_item(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    item_id = request.data.get('item_id')
    try:
        quantity = int(request.data.get('quantity', 1))
    except (TypeError, ValueError):
         return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
    
    if quantity < 1:
        return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    if quantity > cart_item.product.stock_quantity:
        return Response(
            {'error': f'Cannot update quantity. Only {cart_item.product.stock_quantity} in stock.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    cart_item.quantity = quantity
    cart_item.save()
    
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_doc(RemoveCartInputSerializer, CartSerializer, summary="Remove from Cart", description="Remove an item from the cart.")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item_id = request.data.get('item_id')
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)
