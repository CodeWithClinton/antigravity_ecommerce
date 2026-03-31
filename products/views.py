from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.filter(is_active=True)
    
    # Search Filter
    search_query = request.query_params.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)
        
    # Category Filter (supports multiple)
    categories = request.query_params.getlist('category')
    if categories:
        if len(categories) == 1 and ',' in categories[0]:
            categories = categories[0].split(',')
        products = products.filter(category__slug__in=categories)
        
    # Price Range Filter
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    if min_price is not None:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price is not None:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
            
    # Sorting
    sort_option = request.query_params.get('sort', 'newest')
    if sort_option == 'price-asc':
        products = products.order_by('price')
    elif sort_option == 'price-desc':
        products = products.order_by('-price')
    elif sort_option == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')
        
    paginator = StandardResultsSetPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_search(request):
    query = request.query_params.get('q', '')
    products = Product.objects.filter(is_active=True, title__icontains=query).order_by('-created_at')
    
    paginator = StandardResultsSetPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products(request):
    products = Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:8]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def latest_products(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
