from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=4)
    password = serializers.CharField(required=True, min_length=4)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=4)
    password = serializers.CharField(required=True, min_length=4)
