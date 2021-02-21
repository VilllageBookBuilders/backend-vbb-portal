from rest_framework import serializers
from vbb_backend.session.models import Session
from vbb_backend.session.api.serializers.sessionMentor import (
    MentorSessionListSerializer,
)
from vbb_backend.session.api.serializers.sessionStudent import (
    StudentSessionListSerializer,
)


class SessionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    mentors = MentorSessionListSerializer(many=True, read_only=True)
    students = StudentSessionListSerializer(
        source="slot_to_student", many=True, read_only=True
    )

    class Meta:
        model = Session
        exclude = (
            "deleted",
            "external_id",
        )
