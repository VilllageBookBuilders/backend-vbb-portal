from dry_rest_permissions.generics import DRYPermissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from vbb_backend.session.api.serializers.session import SessionSerializer
from vbb_backend.session.models import Session
from vbb_backend.users.models import UserTypeEnum


class SessionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Session.objects.all()
    permission_classes = [IsAuthenticated, DRYPermissions]
    serializer_class = SessionSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_superuser:
            pass
        elif user.user_type == UserTypeEnum.HEADMASTER.value:
            queryset = queryset.filter(slot__computer__program__program_director=user)
        elif user.user_type == UserTypeEnum.MENTOR.value:
            queryset = queryset.filter(mentors__mentor__user__in=user)
        elif user.user_type == UserTypeEnum.STUDENT.value:
            queryset = queryset.filter(students__student__user__in=user)
        else:
            raise PermissionDenied()
        return queryset
