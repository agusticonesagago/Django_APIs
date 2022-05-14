from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes

from profiles.models import Profile
from profiles.serializers import LoginSerializer, SignUpSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authentication import user as user_permissions


class SignUpApiView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    @swagger_auto_schema(
        operation_description="Creates a Profile and auth_token (if necessary) and returns a Profile.",
        request_body=SignUpSerializer,
        security=[],
        responses={
            201: "User created successfully",
            400: "User with this username already exists",
            500: "Internal server error",
        },
    )
    def post(request, **args):
        """
        Creates a Profile and auth_token (if necessary) and returns a Profile.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        if Profile.objects.filter(user__username=username).exists():
            return Response(
                "User with this username already exists",
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            user = User.objects.create(
                username=username, password=make_password(password)
            )
            token = Token.objects.create(user=user)
            return Response(token.key, status=status.HTTP_201_CREATED)

        return Response(
            "Something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class LoginApiView(APIView):
    permission_classes = ()
    http_method_names = ["post"]

    @staticmethod
    @swagger_auto_schema(
        operation_description="Creates a user auth_token (if necessary) and returns a user.",
        request_body=LoginSerializer,
        security=[],
        responses={
            201: "User retrieved successfully",
            400: "Password is not valid",
            404: "User does not exist",
        },
    )
    def post(request, **args):
        """
        Creates a user auth_token (if necessary) and returns a user.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        profile = Profile.objects.filter(user__username=username).first()

        if not profile:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)

        if check_password(password, profile.user.password):
            token, created = Token.objects.get_or_create(user=profile.user)
            return Response(token.key)

        return Response("Password is not valid", status=status.HTTP_400_BAD_REQUEST)


class ProfilesView(APIView):
    authentication_classes = [user_permissions.UserAuthentication]
    http_method_names = ["get"]

    @staticmethod
    @swagger_auto_schema(
        operation_description="Obtain secret information from users",
        query_serializer=None,
        responses={
            200: "Information retrieved successfully",
            403: "User not authenticated correctly",
        },
    )
    def get(request, **args):
        return Response("Secret information")
