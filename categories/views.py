from rest_framework.decorators import api_view, permission_classes
from django_api_readme.decorators import api_doc
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

@api_doc(None, CategorySerializer, summary="List Categories", description="Get a list of all active categories.")
@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.filter(is_active=True)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_doc(None, CategorySerializer, summary="Category Detail", description="Get details of a specific category.")
@api_view(['GET'])
@permission_classes([AllowAny])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk, is_active=True)
    except Category.DoesNotExist:
        return Response(
            {'error': 'Category not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = CategorySerializer(category)
    return Response(serializer.data)
