from rest_framework.decorators import api_view, permission_classes
from django_api_readme.decorators import api_doc
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart
from decimal import Decimal

@api_doc(None, OrderSerializer, summary="Create Order", description="Create a new order from items in the authenticated user's cart.")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
    cart_items = cart.items.all()
    if not cart_items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Validation Step: Check stock availability and active status
    for item in cart_items:
        if not item.product.is_active:
            return Response(
                {'error': f"Product '{item.product.title}' is no longer available"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if item.quantity > item.product.stock_quantity:
            return Response(
                {'error': f"Not enough stock for '{item.product.title}'. Available: {item.product.stock_quantity}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    # Calculate total securely on backend
    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    
    # Create the Order
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
        status='pending',
        payment_status='pending'
    )
    
    # Map CartItems to permanent historical OrderItems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        
    # Clear cart contents after successful mapping
    cart_items.delete()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_doc(None, OrderSerializer, summary="List Orders", description="Get a list of all orders for the authenticated user.")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_doc(None, OrderSerializer, summary="Order Detail", description="Get details of a specific order.")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.get(id=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
    serializer = OrderSerializer(order)
    return Response(serializer.data)
