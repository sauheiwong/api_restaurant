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
        queryset = Table.objects.all()
        max_no_query = self.request.query_params.get('max_no', None)
        restaurant_query = self.request.query_params.get('restaurant_id', None)
        location_query = self.request.query_params.get('location', None)
        if max_no_query:
            queryset = queryset.filter(max_no__gte=int(max_no_query))
        if restaurant_query:
            queryset = queryset.filter(restaurant_id=restaurant_query)
        if location_query:
            queryset = queryset.filter(restaurant__location__icontains=location_query)
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

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can view all orders.'}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return 

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object().user
        if request.user != user:
            return Response({'error': 'Only superuser can view orders.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can delete orders.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can update orders.'}, status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)

class OrderFoodView(APIView):
    queryset = Order.objects.all()

    def get(self, request):
        food_id = request.data.get('name', None)
        number = int(request.data.get('number', 1))
        no_of_people = int(request.data.get('no_of_people', 1))
        order, created = Order.objects.get_or_create(
            user=request.user,
            no_of_people=no_of_people,
            complete=False
            )
        if food_id:
            order_food, created = OrderFood.objects.get_or_create(food_id=food_id, number=number)
            order.ordered_food.add(order_food)
        serializer = OrderSerializer(order)
        return Response({'order': serializer.data}, status=status.HTTP_200_OK)
        
    def post(self, request):
        return 
