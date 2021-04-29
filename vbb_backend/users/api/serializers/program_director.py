import random
import string

from django.db import transaction
from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from vbb_backend.users.models import ProgramDirector, User, UserTypeEnum


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for x in range(y))


class ProgramDirectorUserSerializer(serializers.ModelSerializer):
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
        attrs["user_type"] = UserTypeEnum.PROGRAM_DIRECTOR.value
        return super().validate(attrs)


class ProgramDirectorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    user = ProgramDirectorUserSerializer(required=True)

    class Meta:
        model = ProgramDirector
        exclude = ("deleted", "external_id")

    def validate(self, attrs):
        user = attrs["user"]
        with transaction.atomic():
            if self.instance:
                user_obj = self.instance.user
                user = ProgramDirectorUserSerializer(user_obj, data=user)
                user.is_valid(raise_exception=True)
                instance = user.save()
                attrs["user"] = instance
            else:
                user = ProgramDirectorUserSerializer(data=user)
                user.is_valid(raise_exception=True)
                instance = user.save(email=random_char(20) + "@vbb.com")
                attrs["user"] = instance

            return super().validate(attrs)