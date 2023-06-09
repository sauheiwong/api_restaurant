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
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can delete restaurants.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class TableView(generics.ListCreateAPIView):
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        max_no_query = request.data.get('max_no', None)
        restaurant_query = request.data.get('restaurant_id', None)
        location_query = request.data.get('location', None)
        available = request.data.get('available', True)
        queryset = Table.objects.filter(available=available)
        if max_no_query:
            try:
                max_no = int(max_no_query)
            except ValueError:
                return Response({'error': 'max_no must be int.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(max_no__gte=max_no)
        if restaurant_query:
            try:
                restaurant_id = int(restaurant_query)
            except ValueError:
                return Response({'error': 'restaurant id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if location_query:
            queryset = queryset.filter(restaurant__location__icontains=location_query)
        return Response({'table': TableSerializer(queryset, many=True).data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create table.'}, status=status.HTTP_403_FORBIDDEN)
        max_no = request.data.get('max_no', None)
        restaurant_id = request.data.get('restaurant_id', None)
        if not max_no:
            return Response({'error': 'max_no is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            max_no = int(max_no)
        except ValueError:
            return Response({'error': 'max_no must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        if not restaurant_id:
            return Response({'error': 'restaurant id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant_id = int(restaurant_id)
        except ValueError:
            return Response({'error': 'restaurant_id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': f'restaurant with id {restaurant_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        table = Table.objects.create(
            max_no = max_no,
            restaurant = restaurant
        )
        return Response({'table': TableSerializer(table).data, 'message': 'success'}, status=status.HTTP_201_CREATED)

class SingleTableView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can edit tables.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can delete restaurants.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

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
    
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can delete types.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class FoodView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Food.objects.all()
        name_query = request.data.get('name', None)
        price_lte = request.data.get('price_lte', None)
        price_gte = request.data.get('price_gte', None)
        point_lte = request.data.get('point_lte', None)
        point_gte = request.data.get('point_gte', None)
        type_id = request.data.get('type_id', None)
        if name_query:
            queryset = queryset.filter(Q(chinese_name__icontains=name_query)|Q(english_name__icontains=name_query))
        if price_gte:
            try:
                price_gte = float(price_gte)
            except ValueError:
                return Response({'error': 'price must be float'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(price__gte=price_gte)
        if price_lte:
            try:
                price_lte = float(price_lte)
            except ValueError:
                return Response({'error': 'price must be float'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(price__lte=price_lte)
        if point_gte:
            try:
                point_gte = float(point_gte)
            except ValueError:
                return Response({'error': 'point must be float'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(ave_point__gte=point_gte)
        if point_lte:
            try:
                point_lte = float(point_lte)
            except ValueError:
                return Response({'error': 'point must be float'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(ave_point__gte=point_lte)
        if type_id:
            try:
                type_id = int(type_id)
            except ValueError:
                return Response({'error': 'type id must be int'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(type_id=type_id)
        return Response({'food': FoodSerializer(queryset, many=True).data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create food.'}, status=status.HTTP_403_FORBIDDEN)
        

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
        for food in order.get_ordered_food().values():
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
        return Response({'message': f'Order is completed. Total price is ${order.total_price}', 'order': OrderSerializer(order).data}, status=status.HTTP_200_OK)

class OrderFoodView(APIView):
    queryset = Order.objects.all()
    permission_classes = []
        
    def post(self, request):
        food_id = request.data.get('food_id', None)
        number = request.data.get('number', 1)
        order_id = request.data.get('order_id', None)
        try:
            number = int(number)
        except ValueError:
            return Response({'error': f'Number must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not order_id:
            return Response({'error': 'Order id miss.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'Order id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
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
        except ValueError:
            return Response({'error': f'Food id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Unavailable.objects.filter(food=food, restaurant=order.table.restaurant).exists():
            return Response({'error': f'Sorry, {food.chinese_name}/{food.english_name} is not available in {order.table.restaurant.name} now.'}, status=status.HTTP_404_NOT_FOUND)
        
        ordered_food = order.get_ordered_food()
        if len(ordered_food) == 0:
            no_ordered_food = 0
        else:
            no_ordered_food = max(ordered_food)+1
        ordered_food[no_ordered_food] = {
            'id': food.id,
            'number': number,
            'price': float(food.price*number)
        }
        print(ordered_food)
        order.set_ordered_dict(ordered_food)
        order.total_price += food.price*number
        order.save()
        return Response({'message': 'success', 'ordered_food': FoodSerializer(food).data, 'number': number}, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request):
        order_no = request.data.get('order_no', None)
        order_id = request.data.get('order_id', None)
        if not order_no:
            return Response({'error': 'Order no miss.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order_no = int(order_no)
        except ValueError:
            return Response({'error': f'Order no must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not order_id:
            return Response({'error': 'Order id miss.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'Order id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        if order.user != request.user:
            return Response({'error': 'This order is not yours.'}, status=status.HTTP_403_FORBIDDEN)
        if order.complete:
            return Response({'error': 'This order has been paid. Please create a new order.'}, status=status.HTTP_400_BAD_REQUEST)
        
        ordered_food = order.get_ordered_food()
        deleted_ordered_food = ordered_food.pop(order_no)
        order.set_ordered_dict(ordered_food)
        order.total_price -= deleted_ordered_food['price']

        return Response({'message': 'success', 'order': OrderSerializer(ordered_food).data}, status=status.HTTP_202_ACCEPTED)

class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = []

    def list(self, request):
        queryset = Comment.objects.all()
        food_name = request.data.get('food_name', None)
        give_point_gte = request.data.get('give_point_gte', None)
        give_point_lte = request.data.get('give_point_lte', None)
        user_id = request.data.get('user_id', None)
        restaurant_id = request.data.get('restaurant_id', None)
        if food_name:
            queryset = queryset.filter(Q(food__chinese_name__icontains=food_name)|Q(food__english_name__icontains=food_name))
        if give_point_gte:
            try:
                queryset = queryset.filter(give_point__gte=float(give_point_gte))
            except ValueError:
                return Response({'error': 'give_point must be float'}, status=status.HTTP_400_BAD_REQUEST)
        if give_point_lte:
            try:
                queryset = queryset.filter(give_point__lte=float(give_point_lte))
            except ValueError:
                return Response({'error': 'give_point must be float'}, status=status.HTTP_400_BAD_REQUEST)
        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(id=int(restaurant_id))
            except Restaurant.DoesNotExist:
                return Response({'error': f'Restaurant with id {restaurant_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({'error': f'Restaurant_id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(Restaurant=restaurant)
        if user_id:
            try:
                user = User.objects.get(id=int(user_id))
            except Restaurant.DoesNotExist:
                return Response({'error': f'User with id {user_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({'error': f'User_id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(user=user)
        return Response({'comment': CommentSerializer(queryset, many=True).data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Please login in first.'}, status=status.HTTP_403_FORBIDDEN)
        food_id = self.request.data.get('food_id', None)
        give_point = self.request.data.get('give_point', None)
        restaurant_id = self.request.data.get('restaurant_id', None)
        comment = self.request.data.get('comment', None)
        if not food_id:
            return Response({'error': 'Food id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not restaurant_id:
            return Response({'error': 'Restaurant id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not give_point:
            return Response({'error': 'Point is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            give_point = float(give_point)
        except ValueError:
            return Response({'error': f'Give_point must be float.'}, status=status.HTTP_400_BAD_REQUEST)
        if give_point < 0 or give_point > 5:
            return Response({'error': 'Point must be between 0 to 5'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant = Restaurant.objects.get(id=int(restaurant_id))
        except Restaurant.DoesNotExist:
            return Response({'error': f'Restaurant with id {restaurant_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'Restaurant_id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            food = Food.objects.get(id=int(food_id))
        except Food.DoesNotExist:
            return Response({'error': f'Food with id {food_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'Food_id must be int.'}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(
            user = request.user,
            food = food,
            restaurant = restaurant,
            comment = comment,
            give_point = give_point
        )
        no_of_comment = food.no_of_comment
        food.ave_point = (float(food.ave_point)*no_of_comment + give_point)/(no_of_comment+1)
        food.no_of_comment = no_of_comment + 1
        food.save()
        return Response({'comment': CommentSerializer(comment).data, 'message': 'success'}, status=status.HTTP_201_CREATED)
        
class SingleCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def update(self, request, *args, **kwargs):
        comment_object = self.get_object()
        if request.user != comment_object.user:
            return Response({'error': 'Only writer can edit.'}, status=status.HTTP_403_FORBIDDEN)
        comment = request.data.get('comment', None)
        if comment:
            comment_object.comment = comment
            comment_object.save()
        return Response({'comment': CommentSerializer(comment_object).data}, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        food = comment.food
        give_point = float(comment.give_point)
        if not request.user.is_superuser and (request.user != comment.user) :
            return Response({'error': 'Only superuser or writer can delete restaurants.'}, status=status.HTTP_403_FORBIDDEN)
        no_of_comment = food.no_of_comment
        food.ave_point = (float(food.ave_point)*no_of_comment - give_point)/(no_of_comment-1)
        food.no_of_comment = no_of_comment - 1
        food.save()
        return super().delete(request, *args, **kwargs)

class UnavailableView(generics.ListCreateAPIView):
    queryset = Unavailable.objects.all()
    serializer_class = UnavailableSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can create.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class SingleUnavailableView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unavailable.objects.all()
    serializer_class = UnavailableSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({'error': 'Only superuser can delete.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)