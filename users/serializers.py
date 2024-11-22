from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User
from users.validators import IsValidPhoneValidator


class UserSerializer(serializers.ModelSerializer):
    """Class for user serialization"""
    phone = serializers.CharField(required=False, validators=[IsValidPhoneValidator()])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        """Hashing password"""
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """serializer for MyTokenObtainPairView"""
    @classmethod
    def get_token(cls, user: User) -> TokenObtainPairSerializer:
        token = super().get_token(user)
        token['username'] = user.username
        token['password'] = user.password
        return token
