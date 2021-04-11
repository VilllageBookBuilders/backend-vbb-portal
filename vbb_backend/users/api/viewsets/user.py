from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from vbb_backend.users.api.serializers.user import CurrentUserSerializer

token_response = openapi.Response("User", CurrentUserSerializer)


class CurrentUserView(APIView):
    @swagger_auto_schema(
        responses={
            200: token_response,
            404: "User Not Found in Database",
            403: "Authorisation Failed",
        },
    )
    def get(self, request):
        return Response(CurrentUserSerializer(request.user).data)
