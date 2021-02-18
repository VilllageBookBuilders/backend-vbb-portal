from rest_framework import serializers

from vbb_backend.program.models import MentorSlotAssociation
from vbb_backend.users.models import Mentor
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from rest_framework.exceptions import ValidationError


class MentorSlotBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Mentor
        exclude = ("deleted", "external_id")


class MentorSlotListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    mentor = MentorSlotBaseSerializer()

    class Meta:
        model = MentorSlotAssociation
        exclude = ("deleted", "external_id")


class MentorSlotSerializer(MentorSlotListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    mentor = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = MentorSlotAssociation
        exclude = ("deleted", "slot", "external_id")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "mentor" in attrs:
            mentor = attrs.pop("mentor")
            mentor_obj = Mentor.objects.filter(external_id=mentor).first()
            if not mentor_obj:
                raise ValidationError(
                    {
                        "mentor": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = mentor_obj
        return super().validate(attrs)
