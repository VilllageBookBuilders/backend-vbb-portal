from rest_framework import serializers

from vbb_backend.program.models import HeadmastersProgramAssociation
from vbb_backend.users.models import Headmaster
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from rest_framework.exceptions import ValidationError


class HeadmasterProgramBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Headmaster
        exclude = ("deleted", "external_id")


class HeadmasterProgramListSerializer(serializers.ModelSerializer): 
    id = serializers.UUIDField(source="external_id", read_only=True)
    headmaster = HeadmasterProgramBaseSerializer()

    class Meta:
        model = HeadmastersProgramAssociation
        exclude = ("deleted", "external_id", "program")


class HeadmasterProgramSerializer(HeadmasterProgramListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    headmaster = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = HeadmastersProgramAssociation
        exclude = ("deleted", "program", "external_id")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "headmaster" in attrs:
            headmaster = attrs.pop("headmaster")
            headmaster_obj = Headmaster.objects.filter(external_id=headmaster).first()
            if not headmaster_obj:
                raise ValidationError(
                    {
                        "headmaster": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = headmaster_obj
        return super().validate(attrs)
