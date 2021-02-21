from dry_rest_permissions.generics import DRYPermissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin

from vbb_backend.session.api.serializers.sessionMentor import (
    MentorSessionListSerializer,
)
from vbb_backend.session.models import Session
from vbb_backend.session.models import MentorSessionAssociation
from vbb_backend.users.models import UserTypeEnum


class MentorSessionViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = MentorSessionAssociation.objects.all()
    permission_classes = [IsAuthenticated, DRYPermissions]
    serializer_class = MentorSessionListSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        session = Session.objects.get(
            external_id=self.kwargs.get("session_external_id")
        )
        queryset = queryset.filter(session=session)
        if user.is_superuser:
            pass
        elif user.user_type == UserTypeEnum.HEADMASTER.value:
            queryset = queryset.filter(
                session__computer__program__program_director=user
            )
        elif user.user_type == UserTypeEnum.MENTOR.value:
            queryset = queryset.filter(mentors__mentor__user__in=user)
        elif user.user_type == UserTypeEnum.STUDENT.value and self.action in [
            "list",
            "retrieve",
        ]:
            queryset = queryset.filter(students__student__user__in=user)
        else:
            raise PermissionDenied()
        return queryset
