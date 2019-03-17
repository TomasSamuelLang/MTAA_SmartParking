from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Parkin_lot
from rest_framework.decorators import api_view
from .serializers import UserSerializer, ParkingLotSerializer
from rest_framework.response import Response

@api_view(['get'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['get'])
def getParkings(request):
    parkings = Parkin_lot.objects.all()
    serializer = ParkingLotSerializer(parkings, many=True)
    return Response(serializer.data)
