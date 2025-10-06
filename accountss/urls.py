"""
URL configuration for accountss project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include   
from django.conf.urls.static import static
from django.conf import settings

from users import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Include URLs from the users app
    # path('accounts/', include('django.contrib.auth.urls')),  # For built-in auth views
    path('menu/', include('menu.urls')),  # Include URLs from the menu app
    path('orders/', include('orders.urls')),  # Include URLs from the orders app
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
