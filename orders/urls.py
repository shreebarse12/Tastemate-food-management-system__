from django.urls import path
from . import views

urlpatterns = [
    path("place/<int:dish_id>/", views.place_order, name="place_order"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("manage/", views.manage_orders, name="manage_orders"),
     path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]