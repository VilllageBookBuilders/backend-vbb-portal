from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from vbb_backend.program.api.serializers.slot import SlotSerializer
from vbb_backend.program.models import Computer, Program, Slot
from vbb_backend.session.api.serializer.sessionrule import SessionRuleSerializer
from vbb_backend.session.models import SessionRule
from vbb_backend.users.models import UserTypeEnum

from drf_yasg.utils import swagger_auto_schema


class SlotViewSet(ModelViewSet):
    queryset = Slot.objects.all()
    permission_classes = [IsAuthenticated, DRYPermissions]
    serializer_class = SlotSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        computer = Computer.objects.get(
            external_id=self.kwargs.get("computer_external_id")
        )

        queryset = queryset.filter(computer=computer)
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(computer__program__program_director=user)
        else:
            raise PermissionDenied()
        return queryset

    def get_computer(self):
        return get_object_or_404(
            Computer, external_id=self.kwargs.get("computer_external_id")
        )

    def perform_create(self, serializer):
        serializer.save(computer=self.get_computer())
