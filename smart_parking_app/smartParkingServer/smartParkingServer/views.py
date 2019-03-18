from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response


@api_view(['get', 'put', 'delete'])
def parkingLotId(request, id):
    try:
        parking = Parkin_lot.objects.get(pk=id)
    except Parkin_lot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        parking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ParkingLotSerializer(parking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = ParkingLotDetails(parking)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['get', 'post'])
def parkingLot(request):
    if request.method == 'GET':
        parkings = Parkin_lot.objects.all()
        serializer = ParkingLotSerializer(parkings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ParkingLotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['post'])
def registerUser(request):
    serializer = UserSerializer(data=request.data)

    try:
        login = User.objects.get(login=request.data.get('login'))
    except User.DoesNotExist:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_409_CONFLICT)


@api_view(['post'])
def loginUser(request):
    try:
        user = User.objects.get(login=request.data.get('login'), password=request.data.get('password'))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data.get('id'),status=status.HTTP_200_OK)


@api_view(['get'])
def searchParkingLot(request, searchText):
    try:
        parking = Parkin_lot.objects.filter(Q(name=searchText) | Q(address=searchText))
    except Parkin_lot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ParkingLotSerializer(parking, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['get', 'post', 'delete'])
def favouriteParking(request, id):

    if request.method == 'DELETE':
        try:
            favourite = Favourite_parking_lot.objects.get(pk=id)
        except Favourite_parking_lot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        favourite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':
        try:
            favourite = Favourite_parking_lot.objects.filter(user=id)
        except Favourite_parking_lot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FavouriteSerializer(favourite, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = FavouriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


