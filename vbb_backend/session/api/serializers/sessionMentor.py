from rest_framework import serializers

from vbb_backend.session.models import MentorSessionAssociation
from vbb_backend.users.models import Mentor
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from rest_framework.exceptions import ValidationError


class MentorSessionBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Mentor
        exclude = ("deleted", "external_id")


class MentorSessionListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    mentor = MentorSessionBaseSerializer()

    class Meta:
        model = MentorSessionAssociation
        exclude = ("deleted", "external_id", "session")
