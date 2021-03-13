from rest_framework import serializers

from vbb_backend.session.models import StudentSessionAssociation
from vbb_backend.users.models import Student
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer


class StudentSessionBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Student
        exclude = ("deleted", "external_id")


class StudentSessionListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    student = StudentSessionBaseSerializer(read_only=True)

    class Meta:
        model = StudentSessionAssociation
        exclude = ("deleted", "external_id", "session")
