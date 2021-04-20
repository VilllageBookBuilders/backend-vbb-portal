from dry_rest_permissions.generics import DRYPermissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vbb_backend.program.api.serializers.programHeadmaster import HeadmasterProgramSerializer
from vbb_backend.program.models import Program, HeadmastersProgramAssociation
from vbb_backend.users.models import UserTypeEnum


class HeadmasterProgramViewSet(ModelViewSet):
    queryset = HeadmastersProgramAssociation.objects.all()
    permission_classes = [IsAuthenticated, DRYPermissions]
    serializer_class = HeadmasterProgramSerializer
    lookup_field = "external_id"

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        program = Program.objects.get(external_id=self.kwargs.get("program_external_id"))
        queryset = queryset.filter(program=program)
        if user.is_superuser:
            pass
        elif user.user_type in [UserTypeEnum.HEADMASTER.value]:
            queryset = queryset.filter(computer__program__program_director=user)
        else:
            raise PermissionDenied()
        return queryset

    def get_program(self):
        return get_object_or_404(
            self.get_queryset(), external_id=self.kwargs.get("program_external_id")
        )

    def perform_create(self, serializer):
        serializer.save(program=self.get_program())
