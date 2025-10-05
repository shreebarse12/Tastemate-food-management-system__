from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from menu.views import canteen_dashboard, public_menu

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('register_canteen/', views.register_canteen, name='register_canteen'),
    path('register_student/', views.register_student, name='register_student'),
    path('public_menu/', public_menu, name='public_menu'),
    path('canteen_dashboard/', canteen_dashboard, name='canteen_dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('profile/', views.profile, name='profile'),

]