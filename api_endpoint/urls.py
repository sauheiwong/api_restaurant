from django.urls import path

from . import views

urlpatterns = [
    path('restaurant', views.RestaurantView.as_view()),
    path('restaurant/<int:pk>', views.SingleRestaurantView.as_view()),

    path('table', views.TableView.as_view()),
    path('table/<int:pk>', views.SingleTableView.as_view()),
]