# menu/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('canteen/<int:canteen_id>/', views.canteen_detail, name='canteen_detail'),
    path('dashboard/', views.canteen_dashboard, name='dashboard'),
    path('dish/<int:pk>/edit/', views.edit_dish, name='edit_dish'),
    path('dish/<int:pk>/delete/', views.delete_dish, name='delete_dish'),
    path('public_menu/', views.public_menu, name='public_menu'),
    path('order/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('order/update/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
]
