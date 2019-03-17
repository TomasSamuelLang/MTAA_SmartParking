from django.db import models

class User(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=32)


class Country(models.Model):
    name = models.CharField(max_length=100)


class Town(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Parkin_lot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    capacity = models.IntegerField()
    actualparkedcars = models.IntegerField()
    town = models.ForeignKey(Town, on_delete=models.CASCADE)


class Photo(models.Model):
    photo = models.CharField(max_length=100)
    parkinglot = models.ForeignKey(Parkin_lot, on_delete=models.CASCADE)


class Favourite_parking_lot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parkinglot = models.ForeignKey(Parkin_lot, on_delete=models.CASCADE)


class Old_capacity_data(models.Model):
    parkedcars = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    parkinglot = models.ForeignKey(Parkin_lot, on_delete=models.CASCADE)