from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    location = models.TextField()

    def __str__(self) -> str:
        return self.name
    
class Table(models.Model):
    max_no = models.SmallIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant')

    def __str__(self) -> str:
        return str(self.restaurant.name)+' '+str(self.max_no)+' table'

