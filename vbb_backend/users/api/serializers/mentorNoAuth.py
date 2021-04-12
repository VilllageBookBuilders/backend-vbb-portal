from django.db.models import fields
from rest_framework import serializers

from vbb_backend.users.api.serializers.mentor import MentorUserSerializer
from vbb_backend.users.models import MentorNoAuth, User, UserTypeEnum

from rest_framework.exceptions import ValidationError
from django.db import transaction


class MentorNoAuthSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    user = MentorUserSerializer(required=True)

    class Meta:
        model = MentorNoAuth
        exclude = ("deleted", "external_id")

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