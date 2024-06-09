from rest_framework import serializers
from backend.models.user import User
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["name", "email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        del validated_data["confirm_password"]
        user = User.objects.create(**validated_data)
        return user
