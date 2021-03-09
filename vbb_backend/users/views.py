import logging

import requests
from django.http import JsonResponse
from django.http.response import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from vbb_backend.users.models import User

LOGGER = logging.getLogger(__name__)


class TokenSample(serializers.Serializer):
    refresh = serializers.CharField()
    token = serializers.CharField()


class RequestSample(serializers.Serializer):
    google_access_token = serializers.CharField()


class UserNotFoundException(Exception):
    pass


class UserNotVerifiedException(Exception):
    pass


token_response = openapi.Response("Token", TokenSample)


class VBBLogin(APIView):
    """
    Returns a valid JWT Access and Refresh Token from a valid Google Access Token After Oauth Completion
    """

    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        request_body=RequestSample,
        responses={
            200: token_response,
            404: "User Not Found in Database",
            400: "Invalid Request",
            403: "Authorisation Failed",
        },
    )
    def post(self, request):
        if "google_access_token" in request.data:
            try:
                token = request.data["google_access_token"]
                auth_url = (
                    "https://oauth2.googleapis.com/tokeninfo?access_token=" + str(token)
                )
                token_info_request = requests.get(auth_url)
                google_response = token_info_request.json()
                if google_response["email_verified"] != "true":
                    raise UserNotVerifiedException("User Not Verified")
                email = google_response["email"]

                user = User.objects.filter(email=email).first()

                if user:
                    return JsonResponse(get_refresh_token(user))
                else:
                    raise UserNotFoundException("User Not Found")
            except UserNotFoundException:
                return HttpResponse(status=404)
            except Exception as e:
                LOGGER.error("User Login with Google Failed Because of {}".format(e))
                return HttpResponse(status=403)
        return HttpResponse(status=400)


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }