from rest_auth.registration.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from vbb_backend.users.models import User
import requests
# from google.oauth2 import id_token

class VBBLogin(LoginView): # accessed from .../api/v1/auth/token, accepts token and returns JWT
    # TODO:make serializer for request

    def post(self, request):

        token = request.POST.get("google_access_token")

        auth_url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + str(token)
        token_info = requests.get(auth_url)
        
        email = token_info.GET.get("email")
        users = User.objects.filter(personal_email = email)

        if len(users) == 1:
            return get_refresh_token(users[0]) # send to function to generate token

        # TODO: handle errors for invalid emails


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token), # lifetime should be specified in settings already
    }