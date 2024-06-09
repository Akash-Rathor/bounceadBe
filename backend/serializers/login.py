from rest_framework import serializers
from django.contrib.auth import authenticate
from backend.models.user import User
from backend.utils.exceptions.http_exception import BadRequestError
from backend.serializers.user import UserSerializer


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    otp = serializers.IntegerField(required=True)

    def validate(self, data):
        mobile = data.get('mobile')
        password = data.get('password')
        otp = data.get('otp')

        if not mobile or not password:
            raise serializers.ValidationError("Mobile and password are required.")

        user = authenticate(mobile=mobile, password=password)
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        user_serializer = UserSerializer(instance=user)
        user_serializer.validate_otp(otp)

        return {
            'user': user
        }
