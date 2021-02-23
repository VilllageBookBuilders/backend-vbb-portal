from django.http.response import HttpResponse
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from vbb_backend.users.models import User
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
import requests


class VBBLogin(View):
    """
    accessed from .../api/v1/auth/token, accepts token and returns JWT
    """

    def post(self, request):
        if "google_access_token" in request.POST:
            try:
                token = request.POST["google_access_token"]
                auth_url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + str(
                    token
                )
                token_info = requests.get(auth_url)
                email = token_info.json().get("email", "")

                if email != "":
                    user = User.objects.filter(email=email).first()

                    if user:
                        return JsonResponse(
                            get_refresh_token(user)
                        )  # send to function to generate token
                    else:
                        return HttpResponse(status=404)
                    # TODO: handle case of either no user associated with email or multiple users associated with email
                else:
                    return HttpResponse(status=403)
            except:
                return HttpResponse(status=403)
        # TODO: handle case where no auth token is posted


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": refresh,
        "access": refresh.access_token,  # lifetime should be specified in settings already
    }
