from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from .models import *
from .serializers import *

# Create your views here.

class RestaurantView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        name_query = self.request.query_params.get('name', None)
        location_query = self.request.query_params.get('location', None)
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        if location_query:
            queryset = queryset.filter(location__icontains=location_query)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create restaurant.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class SingleRestaurantView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can edit restaurants.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class TableView(generics.ListCreateAPIView):
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Table.objects.filter(available=True)
        max_no_query = self.request.query_params.get('max_no', None)
        restaurant_query = self.request.query_params.get('restaurant_id', None)
        if max_no_query:
            queryset = queryset.filter(max_no__gte=int(max_no_query))
        if restaurant_query:
            queryset = queryset.filter(restaurant_id=restaurant_query)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create table.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class SingleTableView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can edit tables.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class TypeView(generics.ListCreateAPIView):
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Type.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(chinese_name__icontains=search_query)|Q(english_name__icontains=search_query))
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create type.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class SingleTypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can edit types.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class FoodView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Food.objects.all()
        name_query = self.request.query_params.get('name', None)
        price_lte = self.request.query_params.get('price_lte', None)
        price_gte = self.request.query_params.get('price_gte', None)
        point_lte = self.request.query_params.get('point_lte', None)
        point_gte = self.request.query_params.get('point_gte', None)
        type_id = self.request.query_params.get('type_id', None)
        if name_query:
            queryset = queryset.filter(Q(chinese_name__icontains=name_query)|Q(english_name__icontains=name_query))
        if price_gte:
            queryset = queryset.filter(price__gte=int(price_gte))
        if price_lte:
            queryset = queryset.filter(price__lte=int(price_lte))
        if point_gte:
            queryset = queryset.filter(ave_point__gte=int(point_gte))
        if point_lte:
            queryset = queryset.filter(ave_point__lte=int(point_lte))
        if type_id:
            queryset = queryset.filter(type_id=int(type_id))
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create food.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class SingleFoodView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can edit Foods.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
