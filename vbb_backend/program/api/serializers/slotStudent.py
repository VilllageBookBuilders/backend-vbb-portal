from rest_framework import serializers

from vbb_backend.program.models import StudentSlotAssociation
from vbb_backend.users.models import Student
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from rest_framework.exceptions import ValidationError


class StudentSlotBaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    profile = UserBareMinimumSerializer(source="user")

    class Meta:
        model = Student
        exclude = ("deleted", "external_id")


class StudentSlotListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    student = StudentSlotBaseSerializer(read_only=True)

    class Meta:
        model = StudentSlotAssociation
        exclude = ("deleted", "external_id", "slot")


class StudentSlotSerializer(StudentSlotListSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    student = serializers.UUIDField(write_only=True, allow_null=False)

    class Meta:
        model = StudentSlotAssociation
        exclude = ("deleted", "slot", "external_id")

    def validate(self, attrs):
        # Clean up Attributes based on what the user can access

        if "student" in attrs:
            student = attrs.pop("student")
            student_obj = Student.objects.filter(external_id=student).first()
            if not student_obj:
                raise ValidationError(
                    {
                        "student": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = student_obj
        return super().validate(attrs)
