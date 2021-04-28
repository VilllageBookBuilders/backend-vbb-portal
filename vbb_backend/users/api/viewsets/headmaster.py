from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vbb_backend.users.api.serializers.headmaster import HeadmasterSerializer
from vbb_backend.program.models import School
from vbb_backend.users.models import Headmaster
from vbb_backend.users.models import UserTypeEnum


class HeadmasterViewSet(ModelViewSet):
    queryset = Headmaster.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = HeadmasterSerializer
    lookup_field = "external_id"

    def get_permissions(self):
        if self.action == "create":
            return []
        return super().get_permissions()

    def get_queryset(self):
        queryset = self.queryset.filter(user__user_type=UserTypeEnum.HEADMASTER.value)
        user = self.request.user
        if user.is_superuser:
            pass
        else:
            queryset = self.queryset.filter(user=user)
        return queryset
