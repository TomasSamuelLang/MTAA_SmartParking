from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth import models as authmodels


class UserSerializer(ModelSerializer):
    class Meta:
        model = authmodels.User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class ParkingLotSerializer(ModelSerializer):
    class Meta:
        model = Parkin_lot
        fields = '__all__'


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class TownSerializer(ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Town
        fields = '__all__'


class ParkingLotDetails(ModelSerializer):
    parkinglot = PhotoSerializer(read_only=True, many=True)
    town = TownSerializer(read_only=True)

    class Meta:
        model = Parkin_lot
        #fields = ('id', 'name', 'address', 'capacity', 'actualparkedcars', 'town', 'photo')
        fields = "__all__"


class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite_parking_lot
        fields = "__all__"
