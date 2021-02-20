from rest_framework import serializers

from vbb_backend.program.models import Program
from vbb_backend.users.api.serializers.user import UserBareMinimumSerializer
from vbb_backend.users.models import User

from rest_framework.exceptions import ValidationError


class ProgramSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    program_director = serializers.UUIDField(write_only=True, allow_null=False)
    program_director_obj = UserBareMinimumSerializer(
        source="program_director", read_only=True
    )

    class Meta:
        model = Program
        exclude = ("deleted", "external_id")

    def validate(self, attrs):
        user = self.context["request"].user
        # Clean up Attributes based on what the user can access
        if not user.is_superuser:
            for attribute in Program.ACCESS_CONTROL:
                if attribute in attrs:
                    if user.user_type not in Program.ACCESS_CONTROL[attribute]:
                        attrs.pop(attribute)

        if "program_director" in attrs:
            program_director_external_id = attrs.pop("program_director")
            product_director_obj = User.objects.filter(
                external_id=program_director_external_id
            ).first()
            if not product_director_obj:
                raise ValidationError(
                    {
                        "program_director": "Does not Exist. Are you sure the supplied value is a valid UUID"
                    }
                )
            attrs["program_director"] = product_director_obj
        return super().validate(attrs)


class MinimalProgramSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    program_director = serializers.UUIDField(write_only=True, allow_null=False)
    program_director_obj = UserBareMinimumSerializer(
        source="program_director", read_only=True
    )

    class Meta:
        model = Program
        exclude = ("deleted", "external_id")