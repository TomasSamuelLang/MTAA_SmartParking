from django.contrib.auth import authenticate
from django.db.models import Q
from pytz import unicode
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import models as authmodels


@api_view(['put'])
def postPhoto(request):
    try:
        photo = Photo.objects.get(parkinglot=request.data.get('parkinglot'))
    except Photo.DoesNotExist:
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    photo.image = request.data.get('image')
    photo.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['get'])
def get_photo(request, id):
    try:
        photo = Photo.objects.get(parkinglot=id)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = PhotoSerializer(photo)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
@permission_classes((AllowAny,))
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['get'])
def getAllTowns(request):
    towns = Town.objects.all()
    serializer = TownSerializer(towns, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['post', 'get'])
@permission_classes((AllowAny,))
def getTownId(request):

    if request.method == 'POST':
        try:
            result = Town.objects.all().get(name=request.data.get('name'))
        except Town.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = TownSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_409_CONFLICT)


@api_view(['post'])
@permission_classes((AllowAny,))
def registerUser(request):

    password = make_password(request.data.get('password'))
    user = {"username": request.data.get('username'), "password": password}

    serializer = UserSerializer(data=user)

    if serializer.is_valid():
        user = serializer.save()
        if user:
            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] = token.key
            return Response(json, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginUser(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    user = authmodels.User.objects.all().get(username=username)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'id': user.id, "username": user.username},
                    status=status.HTTP_200_OK)


@api_view(['get'])
@permission_classes((AllowAny,))
def searchParkingLot(request, searchText):
    try:
        parking = Parkin_lot.objects.filter(Q(name=searchText) | Q(address=searchText))
    except Parkin_lot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ParkingLotSerializer(parking, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['get', 'post', 'delete'])
@permission_classes((AllowAny,))
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


