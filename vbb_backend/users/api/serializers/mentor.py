from django.db.models import fields
from rest_framework import serializers

from vbb_backend.users.models import Mentor, User, UserTypeEnum

from rest_framework.exceptions import ValidationError
from django.db import transaction


class MentorUserSerializer(serializers.ModelSerializer):
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
        attrs["user_type"] = UserTypeEnum.MENTOR.value
        return super().validate(attrs)


class MentorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    user = MentorUserSerializer(required=True)

    class Meta:
        model = Mentor
        exclude = ("deleted", "school")

    def validate(self, attrs):
        user = attrs["user"]
        with transaction.atomic():
            if self.instance:
                user_obj = self.instance.user
                user = MentorUserSerializer(user_obj, data=user)
                user.is_valid(raise_exception=True)
                instance = user.save()
                attrs["user"] = instance
            else:
                user = MentorUserSerializer(data=user)
                user.is_valid(raise_exception=True)
                instance = user.save()
                attrs["user"] = instance

            return super().validate(attrs)