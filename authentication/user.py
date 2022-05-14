from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_token = request.META.get("HTTP_USER_TOKEN")
        if not user_token:
            raise exceptions.AuthenticationFailed(f"Token was not provided")

        try:
            user = Token.objects.filter(key=user_token).first().user
        except Exception as e:
            raise exceptions.AuthenticationFailed(
                "User with the provided token does not exist"
            )

        return user, None
