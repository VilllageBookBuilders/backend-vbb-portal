from django.db import models

from vbb_backend.utils.models.base import BaseUUIDModel

from vbb_backend.program.models import Slot

from vbb_backend.users.models import User


# class SessionRule(BaseUUIDModel):
#     """
#     This Model represents the start of a Session which can go on indefenitely or be deleted at some point
#     The Session Rule will be tied to a Library Computer Slot
#     """

#     slot = models.ForeignKey(
#         Slot, on_delete=models.SET_NULL, null=True
#     )  # Represents the Connected Slot
#     start = models.DateTimeField()  # All Date Times in UTC
#     end = models.DateTimeField(null=True, blank=True)  # All Date Times in UTC


class Session(BaseUUIDModel):
    """
    This Model represents the sessions history and the next upcoming session for mentors.
    An Asyncronous task will populate the required sessions from the SessionRule
    """

    slot = models.ForeignKey(
        Slot, on_delete=models.SET_NULL, null=True
    )  # Represents the Connected Slot
    notes = models.TextField(default=None, null=True, blank=True)
    start = models.DateTimeField()  # All Date Times in UTC
    end = models.DateTimeField()  # All Date Times in UTC
    students = models.ManyToManyField(
        "users.Student", through="StudentSessionAssociation"
    )
    mentors = models.ManyToManyField("users.Mentor", through="MentorSessionAssociation")


class StudentSessionAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Session Object
    """

    student = models.ForeignKey(
        "users.Student",
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_session",
    )
    session = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True, related_name="session_student"
    )
    attended = models.BooleanField(default=False)


class MentorSessionAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Session Object
    """

    mentor = models.ForeignKey(
        "users.Mentor",
        on_delete=models.SET_NULL,
        null=True,
        related_name="mentor_session",
    )
    session = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True, related_name="session_mentor"
    )
    attended = models.BooleanField(default=False)
