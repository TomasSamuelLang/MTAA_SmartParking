from rest_framework.serializers import ModelSerializer
from .models import User, Parkin_lot

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ParkingLotSerializer(ModelSerializer):
    class Meta:
        model = Parkin_lot
        fields = '__all__'
