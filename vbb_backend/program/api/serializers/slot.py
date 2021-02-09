from rest_framework import serializers
from datetime import datetime, timedelta
from vbb_backend.program.models import Slot
from rest_framework.exceptions import ValidationError
from vbb_backend.program.api.serializers.slotMentor import MentorSlotListSerializer
from vbb_backend.program.api.serializers.slotStudent import StudentSlotListSerializer


class SlotSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    start_day_of_the_week = serializers.IntegerField(
        min_value=0,
        max_value=6,
        required=True,
        help_text="Week Starts with Monday (0), Convert Time to UTC First",
    )
    end_day_of_the_week = serializers.IntegerField(
        min_value=0,
        max_value=6,
        help_text="Week Starts with Monday (0), Convert Time to UTC first",
    )
    start_hour = serializers.IntegerField(
        min_value=0,
        max_value=23,
        required=True,
        help_text="0-23 Hours, Convert Time to UTC First",
    )
    start_minute = serializers.IntegerField(
        min_value=0, max_value=59, help_text="0-59 Minutes, Convert Time to UTC First"
    )
    end_hour = serializers.IntegerField(
        min_value=0, max_value=23, help_text="0-23 Hours, Convert Time to UTC First"
    )
    end_minute = serializers.IntegerField(
        min_value=0, max_value=59, help_text="0-59 Minutes, Convert Time to UTC First"
    )
    max_students = serializers.IntegerField(min_value=0)

    mentors = MentorSlotListSerializer(
        source="slot_to_mentor", many=True, read_only=True
    )
    students = StudentSlotListSerializer(
        source="slot_to_student", many=True, read_only=True
    )

    def validate(self, attrs):
        start_day_of_week = attrs.pop("start_day_of_the_week")
        start_hour = attrs.pop("start_hour")
        start_minute = attrs.pop("start_minute")

        end_day_of_week = attrs.pop("end_day_of_the_week")
        end_hour = attrs.pop("end_hour")
        end_minute = attrs.pop("end_minute")

        schedule_start = Slot.DEAFULT_INIT_DATE + timedelta(
            days=start_day_of_week, hours=start_hour, minutes=start_minute
        )
        schedule_end = Slot.DEAFULT_INIT_DATE + timedelta(
            days=end_day_of_week, hours=end_hour, minutes=end_minute
        )

        if schedule_start >= schedule_end:
            raise ValidationError(
                {"schedule": "End of Schedule must be greater than Start of Schedule"}
            )
        validated_data = super().validate(attrs)

        validated_data["schedule_start"] = schedule_start
        validated_data["schedule_end"] = schedule_end
        return validated_data

    class Meta:
        model = Slot
        exclude = (
            "deleted",
            "computer",
            "external_id",
            "schedule_start",
            "schedule_end",
        )
        read_only_fields = (
            "is_mentor_assigned",
            "is_student_assigned",
            "assigned_students",
        )
