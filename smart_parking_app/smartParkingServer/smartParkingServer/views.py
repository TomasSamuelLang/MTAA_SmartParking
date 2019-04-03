from django.contrib.auth import authenticate
from django.db.models import Q
from pytz import unicode
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError


@api_view(['post'])
def postPhoto(request):
    parser_class = (FileUploadParser,)

    if 'file' not in request.data:
        raise ParseError("Empty content")

    return

@api_view(['get'])
def get_photo(request, id):

    photo = Photo.objects.get(parkinglot=id)

    serializer = PhotoSerializer(photo)

    return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['post', 'get'])
def getTownId(request):

    if request.method == 'POST':
        try:
            town = Town.objects.get(name=request.data.get('name'))
        except town is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = TownSerializer(town);
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_409_CONFLICT)


@api_view(['post'])
def registerUser(request):

    password = make_password(request.data.get('password'))
    user = {"login": request.data.get('login'), "password": password}

    serializer = UserSerializer(data=user)

    try:
        User.objects.get(login=request.data.get('login'))
    except User.DoesNotExist:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


@api_view(['post'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def loginUserSuper(request):

    login = request.data.get("login")
    password = request.data.get("password")

    user2 = authenticate(username=login, password=password)

    if not user2:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user2)

    return Response(status=status.HTTP_200_OK)

@api_view(['post'])
def loginUser(request):

    try:
        user = User.objects.get(login=request.data.get('login'))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if check_password(request.data.get('password'), user.password):

        serializer = UserSerializer(user)

        return Response(serializer.data.get('id'), status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

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


