from django.urls import path

from . import views

urlpatterns = [
    path('restaurant', views.RestaurantView.as_view()),
    path('restaurant/<int:pk>', views.SingleRestaurantView.as_view()),

    path('table', views.TableView.as_view()),
    path('table/<int:pk>', views.SingleTableView.as_view()),

    path('type', views.TypeView.as_view()),
    path('type/<int:pk>', views.SingleTypeView.as_view()),

    path('food', views.FoodView.as_view()),
    path('food/<int:pk>', views.SingleFoodView.as_view()),

    path('order', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),

    path('order-food', views.OrderFoodView.as_view()),
]