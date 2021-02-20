from rest_framework import serializers

from vbb_backend.program.models import Computer

from vbb_backend.program.api.serializers.program import (
    MinimalProgramSerializer,
)


class ComputerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    class Meta:
        model = Computer
        exclude = ("deleted", "program", "external_id")


class MinimalComputerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    program = MinimalProgramSerializer()

    class Meta:
        model = Computer
        exclude = ("deleted", "external_id")