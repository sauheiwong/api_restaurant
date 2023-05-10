from rest_framework import serializers

from .models import *

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location']

class TableSerializer(serializers.ModelSerializer):
    # restaurant = serializers.PrimaryKeyRelatedField(
	# 		queryset=Restaurant.objects.all(), many=False
	# )
    # restaurant = RestaurantSerializer()
    class Meta:
        model = Table
        fields = ['id', 'max_no', 'restaurant']