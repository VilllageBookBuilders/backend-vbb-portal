from rest_framework import serializers

from vbb_backend.users.models import User, UserTypeChoices
from vbb_backend.utils.serializers import ChoiceField


class UserBareMinimumSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "id", "external_id")


class CurrentUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    user_type = ChoiceField(choices=UserTypeChoices)

    class Meta:
        model = User
        fields = ("user_type", "email", "first_name", "last_name", "id", "external_id")
