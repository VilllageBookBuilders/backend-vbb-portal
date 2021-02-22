from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from vbb_backend.users.models import User
from django.http import HttpResponse
import requests

class VBBLogin(View): # accessed from .../api/v1/auth/token, accepts token and returns JWT
    def post(self, request):
        token = request.POST.get('google_access_token','')
        if token != '':
            auth_url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + str(token)
            token_info = requests.get(auth_url)
            email = token_info.json().get('email', '')

            if email != '':
                users = User.objects.filter(personal_email = email)

                if len(users) == 1:
                    return HttpResponse(get_refresh_token(users[0])) # send to function to generate token
                else:
                    return HttpResponse('Error: no user associated with email') 
                # TODO: handle case of either no user associated with email or multiple users associated with email
            else:
                return HttpResponse('Error: no email associated with auth token')
        
        # TODO: handle case where no auth token is posted


def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': refresh,
        'access': refresh.access_token, # lifetime should be specified in settings already
    }
        