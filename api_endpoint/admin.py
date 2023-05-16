from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Type)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Unavailable)