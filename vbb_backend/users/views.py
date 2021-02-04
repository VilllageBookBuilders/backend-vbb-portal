from rest_auth.registration.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
# from google.oauth2 import id_token

class VBBLogin(LoginView): # accessed from .../api/v1/auth/token, accepts token and returns JWT

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def post(request):
        # user =  id_token.verify_oauth2_token(request.token) # send token field to OAuth to retrieve user
        return get_refresh_token(user) # send to function to generate token

def get_refresh_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token), # lifetime should be specified in settings already
    }