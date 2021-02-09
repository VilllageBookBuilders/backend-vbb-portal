from rest_framework import serializers

from vbb_backend.program.models import MentorSlotAssociation
from vbb_backend.users.models import Mentor
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer


class MentorSlotBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Mentor
        exclude = ("deleted", "external_id")


class MentorSlotSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    mentor = MentorSlotBaseSerializer()

    class Meta:
        model = MentorSlotAssociation
        exclude = ("deleted", "external_id")
