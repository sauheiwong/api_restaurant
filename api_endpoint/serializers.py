from rest_framework import serializers

from .models import *

class RestaurantByTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location']
        extra_kwargs = {
            'name': {'read_only': True},
            'location': {'read_only': True}
        }

class TableSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), write_only=True) #write
    restaurant_info = RestaurantByTableSerializer(source='restaurant', read_only=True) # read
    class Meta:
        model = Table
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    own_by = TableSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'own_by']

class FoodByTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    type = FoodByTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Type
        fields = '__all__'

class TypeByFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'chinese_name', 'english_name']

class FoodSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), write_only=True)
    type_info = TypeByFoodSerializer(source='type', read_only=True)
    class Meta:
        model = Food
        fields = '__all__'
        extra_kwargs = {
            'ave_point': {'read_only': True},
        }

class FoodByOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        exclude = ['type']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
			queryset=User.objects.all(),
			default=serializers.CurrentUserDefault()
	)
    table = TableSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    food = FoodByOrderSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
