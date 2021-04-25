from rest_framework import serializers

from vbb_backend.program.models import ManagersProgramAssociation
from vbb_backend.users.models import ProgramManager
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from rest_framework.exceptions import ValidationError


class ManagerProgramBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = ProgramManager
        exclude = ("deleted", "external_id")


class ManagerProgramListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    manager = ManagerProgramBaseSerializer()

    class Meta:
        model = ManagersProgramAssociation
        exclude = ("deleted", "external_id", "program")


class ManagerProgramSerializer(ManagerProgramListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    Manager = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = ManagersProgramAssociation
        exclude = ("deleted", "program", "external_id")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "manager" in attrs:
            manager = attrs.pop("manager")
            manager_obj = ProgramManager.objects.filter(external_id=Manager).first()
            if not manager_obj:
                raise ValidationError(
                    {
                        "manager": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = manager_obj
        return super().validate(attrs)


class ManagerProgramBookingSerializer(ManagerProgramListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    manager = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = ManagersProgramAssociation
        exclude = ("deleted", "program", "external_id", "is_confirmed", "priority")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "manager" in attrs:
            manager = attrs.pop("manager")
            manager_obj = ProgramManager.objects.filter(external_id=manager).first()
            if not manager_obj:
                raise ValidationError(
                    {
                        "manager": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = manager_obj
        return super().validate(attrs)
