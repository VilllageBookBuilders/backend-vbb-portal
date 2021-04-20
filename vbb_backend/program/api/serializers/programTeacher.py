from rest_framework import serializers

from vbb_backend.program.models import TeachersProgramAssociation
from vbb_backend.users.models import Teacher
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from rest_framework.exceptions import ValidationError


class TeacherProgramBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Teacher
        exclude = ("deleted", "external_id")


class TeacherProgramListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    teacher = TeacherProgramBaseSerializer()

    class Meta:
        model = TeachersProgramAssociation
        exclude = ("deleted", "external_id", "program")


class TeacherProgramSerializer(TeacherProgramListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    teacher = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = TeachersProgramAssociation
        exclude = ("deleted", "program", "external_id")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "teacher" in attrs:
            teacher = attrs.pop("teacher")
            teacher_obj = Teacher.objects.filter(external_id=teacher).first()
            if not teacher_obj:
                raise ValidationError(
                    {
                        "teacher": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = teacher_obj
        return super().validate(attrs)


class TeacherProgramBookingSerializer(TeacherProgramListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    teacher = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = TeachersProgramAssociation
        exclude = ("deleted", "program", "external_id", "is_confirmed", "priority")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "teacher" in attrs:
            teacher = attrs.pop("teacher")
            teacher_obj = Teacher.objects.filter(external_id=teacher).first()
            if not teacher_obj:
                raise ValidationError(
                    {
                        "teacher": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = teacher_obj
        return super().validate(attrs)
