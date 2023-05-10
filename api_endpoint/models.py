from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    location = models.TextField()

    def __str__(self) -> str:
        return self.name
    
class Table(models.Model):
    max_no = models.SmallIntegerField()
    available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='own_by')

    def __str__(self) -> str:
        return str(self.restaurant.name)+' '+str(self.max_no)+' table'

class Type(models.Model):
    chinese_name = models.CharField(max_length=64)
    english_name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.english_name+' '+self.chinese_name

class Food(models.Model):
    chinese_name = models.CharField(max_length=64)
    english_name = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField(default='', null=True, blank=True)
    ave_point = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type')

    def __str__(self) -> str:
        return self.english_name
    
class Unavailable(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='unavailable_food')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='unavailable_restaurant')

    def __str__(self) -> str:
        return self.restaurant.name+' can not provide '+self.food.english_name

class OrderFood(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='ordered_food')
    no = models.SmallIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self) -> str:
        return str(self.no)+' '+self.food.english_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table')
    ordered_food = models.ManyToManyField(OrderFood, related_name='ordered_food')
    no_of_people = models.SmallIntegerField()
    complete = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=71)

    def __str__(self) -> str:
        return self.table+' with '+str(self.no_of_people)+' '+self.total_price

