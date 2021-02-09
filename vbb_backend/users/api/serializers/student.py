from django.db.models import fields
from rest_framework import serializers

from vbb_backend.users.models import Student, User, UserTypeEnum

from rest_framework.exceptions import ValidationError


class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "time_zone",
            "initials",
            "personal_email",
            "phone",
            "city",
            "notes",
        )

    def validate(self, attrs):
        attrs["user_type"] = UserTypeEnum.STUDENT.value
        return super().validate(attrs)


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    user = StudentUserSerializer(required=True)

    class Meta:
        model = Student
        exclude = ("deleted", "school")

    def validate(self, attrs):
        user = attrs["user"]
        if self.instance:
            user_obj = self.instance.user
            user = StudentUserSerializer(user_obj, data=user)
            user.is_valid(raise_exception=True)
            instance = user.save()
            attrs["user"] = instance
        else:
            user = StudentUserSerializer(data=user)
            user.is_valid(raise_exception=True)
            instance = user.save()
            attrs["user"] = instance

        return super().validate(attrs)