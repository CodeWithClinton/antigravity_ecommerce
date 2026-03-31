import os
import uuid
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from orders.models import Order
from .models import Payment

PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', 'sk_test_placeholder')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({'error': 'order_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Fetch Order ensuring ownership
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # 2. Prevent initiating payment on paid orders
    if order.payment_status != 'pending':
        return Response({'error': 'Order is not pending payment'}, status=status.HTTP_400_BAD_REQUEST)
        
    # 3. Reference generation 
    reference = str(uuid.uuid4())
    
    # 4. Paystack API payload map
    amount_in_kobo = int(order.total_amount * 100)
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": request.user.email,
        "amount": amount_in_kobo,
        "reference": reference
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
    except Exception as e:
        return Response(
            {'error': 'Failed to communicate with payment gateway'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    if not response_data.get('status'):
        return Response(
            {'error': response_data.get('message', 'Payment initiation failed')}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # 5. Persist the Payment record natively
    Payment.objects.create(
        order=order,
        reference=reference,
        amount=order.total_amount,
        status='pending'
    )
    
    auth_url = response_data['data']['authorization_url']
    access_code = response_data['data']['access_code']
    
    return Response({
        'authorization_url': auth_url,
        'access_code': access_code,
        'reference': reference
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    reference = request.data.get('reference')
    if not reference:
        return Response({'error': 'reference is required'}, status=status.HTTP_400_BAD_REQUEST)

    payment = get_object_or_404(Payment, reference=reference, order__user=request.user)

    if payment.status == 'successful':
        return Response({'message': 'Payment already verified successfully'}, status=status.HTTP_200_OK)

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
    except Exception as e:
        return Response(
            {'error': 'Failed to communicate with payment gateway'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    api_status = response_data.get('status')
    if not api_status:
        return Response(
            {'error': response_data.get('message', 'Verification request failed')}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    data = response_data.get('data', {})
    tx_status = data.get('status')
    amount_in_kobo = data.get('amount')

    # Guard securely against request payload manipulation
    if amount_in_kobo != int(payment.amount * 100):
        return Response({'error': 'Transaction amount mismatch'}, status=status.HTTP_400_BAD_REQUEST)

    if tx_status == 'success':
        try:
            with transaction.atomic():
                payment.status = 'successful'
                payment.save()

                order = payment.order
                order.payment_status = 'paid'
                order.status = 'paid'
                order.save()

                for item in order.items.all():
                    if item.product:
                        item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
                        item.product.save()

            return Response({'message': 'Payment successful and order updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to process successful payment internally'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif tx_status in ['failed', 'abandoned']:
        payment.status = 'failed'
        payment.save()
        return Response({'error': f'Payment {tx_status}'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': f'Payment is currently {tx_status}'}, status=status.HTTP_200_OK)
