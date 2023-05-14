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
        max_no_query = self.request.data.get('max_no', None)
        restaurant_query = self.request.data.get('restaurant_id', None)
        location_query = self.request.data.get('location', None)
        available = self.request.data.get('available', True)
        queryset = Table.objects.filter(available=available)
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
        table, no_of_people = int(request.data.get('table_id', None)), int(request.data.get('no_of_people', 1))
        if not table:
            return Response({'error': 'Table id miss'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            table = Table.objects.get(id=table)
            if no_of_people > table.max_no:
                return Response({'error': f'The max. load of this table ({table.max_no}) is smaller than {no_of_people}.'}, status=status.HTTP_404_NOT_FOUND)
            table.available = False
            table.save()
        except Table.DoesNotExist:
            return Response({'error': 'Table id does not exist'}, status=status.HTTP_404_NOT_FOUND)
        order = Order.objects.create(
            user=request.user,
            table=table,
            no_of_people=no_of_people,
        )
        return Response({'order': OrderSerializer(order).data}, status=status.HTTP_201_CREATED)

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user != order.user and not request.user.is_superuser:
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
    permission_classes = []

    # def get(self, request):
    #     order_id = request.data.get('order_id', None)
    #     if not order_id:
    #         return Response({'error': 'Order id miss.'}, status=status.HTTP_400_BAD_REQUEST)
    #     try:
    #         order = Order.objects.get(id=int(order_id))
    #     except Order.DoesNotExist:
    #         return Response({'error': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    #     if order.user != request.user and not request.user.is_superuser:
    #         return Response({'error': 'This order is not yours.'}, status=status.HTTP_403_FORBIDDEN)
        
    #     return
        
    def post(self, request):
        food_id = request.data.get('food_id', None)
        number = int(request.data.get('number', 1))
        order_id = request.data.get('order_id', None)
        if not order_id:
            return Response({'error': 'Order id miss.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if order.user != request.user:
            return Response({'error': 'This order is not yours.'}, status=status.HTTP_403_FORBIDDEN)
        if not food_id:
            return Response({'error': 'food id miss.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            food = Food.objects.get(id=int(food_id))
        except Food.DoesNotExist:
            return Response({'error': f'Food id {food_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        order_food, created = OrderFood.objects.get_or_create(food=food, no=number)
        order.ordered_food.add(order_food)
        total = 0
        for order_food in order.ordered_food.all():
            food_price = order_food.food.price
            no = order_food.no
            total += food_price*no
        order.total_price = total
        order.save()
        return Response({'ordered_food': OrderFoodSerializer(order_food).data, 'message': 'success'}, status=status.HTTP_201_CREATED)
