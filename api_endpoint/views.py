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
        name_query = self.request.data.get('name', None)
        location_query = self.request.data.get('location', None)
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
        search_query = self.request.data.get('search', None)
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
        name_query = self.request.data.get('name', None)
        price_lte = self.request.data.get('price_lte', None)
        price_gte = self.request.data.get('price_gte', None)
        point_lte = self.request.data.get('point_lte', None)
        point_gte = self.request.data.get('point_gte', None)
        type_id = self.request.data.get('type_id', None)
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
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can edit Foods.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can view all orders.'}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        table, no_of_people = request.data.get('table_id', None), int(request.data.get('no_of_people', 1))
        if not table:
            return Response({'error': 'Table id miss'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            table = Table.objects.get(id=int(table))
            if no_of_people > table.max_no:
                return Response({'error': f'The max. load of this table ({table.max_no}) is smaller than {no_of_people}.'}, status=status.HTTP_404_NOT_FOUND)
            if not table.available:
                return Response({'error': f'This table is not available now. Please choice other table.'}, status=status.HTTP_403_FORBIDDEN)
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
        ordered_food = []
        for food in order.get_ordered_food():
            food_infor = Food.objects.get(id=food['id'])
            ordered_food.append(
                {
                    'chinese_name': food_infor.chinese_name,
                    'english_name': food_infor.english_name,
                    'number': food['number']
                }
            )
        data = {
            'order': OrderSerializer(order).data,
            'ordered_food': ordered_food
        }
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can delete orders.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can update orders.'}, status=status.HTTP_403_FORBIDDEN)
        complete = request.data.get('complete', False)
        if not complete:
            return Response({'message': 'Order still lives.'}, status=status.HTTP_200_OK)
        order = self.get_object()
        order.complete = True
        order.save()
        return Response({'message': f'Order is completed. Total price is ${order.total_price}'}, status=status.HTTP_200_OK)

class OrderFoodView(APIView):
    queryset = Order.objects.all()
    permission_classes = []
        
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
        if order.complete:
            return Response({'error': 'This order has been paid. Please create a new order.'}, status=status.HTTP_400_BAD_REQUEST)
        if not food_id:
            return Response({'error': 'food id miss.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            food = Food.objects.get(id=int(food_id))
        except Food.DoesNotExist:
            return Response({'error': f'Food id {food_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        ordered_food = order.get_ordered_food()
        ordered_food.append(
            {
                'id': food.id,
                'number': number
            }
        )
        order.set_ordered_list(ordered_food)
        order.total_price += food.price*number
        order.save()
        return Response({'message': 'success', 'ordered_food': FoodSerializer(food).data, 'number': number}, status=status.HTTP_202_ACCEPTED)

class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Comment.objects.all()
        food_name = self.request.data.get('food_name', None)
        give_point = self.request.data.get('give_point', None)
        user = self.request.data.get('user', None)
        restaurant_id = self.request.data.get('restaurant_id', None)
        if food_name:
            queryset = queryset.filter(Q(ate__chinese_name__icontains=food_name)|Q(ate__english_name__icontains=food_name))
        if give_point:
            queryset = queryset.filter(give_point__gte=float(give_point))
        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(id=int(restaurant_id))
            except Restaurant.DoesNotExist:
                return Response({'error': f'Restaurant with id {restaurant_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            queryset = queryset.filter(Restaurant=restaurant)
        return queryset
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Please login in first.'}, status=status.HTTP_403_FORBIDDEN)
        food_id = self.request.data.get('food_id', None)
        give_point = self.request.data.get('give_point', None)
        restaurant_id = self.request.data.get('restaurant_id', None)
        comment = self.request.data.get('comment', None)
        if not food_id:
            return Response({'error': 'Food id required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not restaurant_id:
            return Response({'error': 'Restaurant id required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not give_point:
            return Response({'error': 'Point required.'}, status=status.HTTP_400_BAD_REQUEST)
        give_point = float(give_point)
        if give_point < 0 or give_point > 5:
            return Response({'error': 'Point must be between 0 to 5'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant = Restaurant.objects.get(id=int(restaurant_id))
        except Restaurant.DoesNotExist:
            return Response({'error': f'Restaurant with id {restaurant_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            food = Food.objects.get(id=int(food_id))
        except Food.DoesNotExist:
            return Response({'error': f'Food with id {food_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.create(
            user = request.user,
            food = food,
            Restaurant = restaurant,
            comment = comment,
            give_point = give_point
        )
        no_of_comment = food.no_of_comment
        food.ave_point = (float(food.ave_point)*no_of_comment + give_point)/(no_of_comment+1)
        food.no_of_comment = no_of_comment + 1
        food.save()
        return Response({'comment': CommentSerializer(comment).data, 'message': 'success'}, status=status.HTTP_201_CREATED)
        
        
