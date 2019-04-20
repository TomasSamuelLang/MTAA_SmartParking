"""smartParkingServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # path('authenticate/', loginUserSuper),
    path('admin/', admin.site.urls),
    path('getusers/', getUsers),
    path('registeruser/', registerUser),
    path('loginuser/', loginUser),
    path('searchparking/<str:searchText>', searchParkingLot),
    path('favouriteparkinglot/<int:id>', favouriteParking),
    path('parkinglot/<int:id>', parkingLotId),
    path('parkinglot/', parkingLot),
    path('gettownid/', getTownId),
    path('getphoto/<int:id>', get_photo),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
