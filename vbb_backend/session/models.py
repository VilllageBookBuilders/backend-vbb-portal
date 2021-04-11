from django.db import models

from vbb_backend.utils.models.base import BaseUUIDModel

from vbb_backend.program.models import Computer, Slot

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

    computer = models.ForeignKey(Computer, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()  # All Date Times in UTC
    end = models.DateTimeField()  # All Date Times in UTC
    students = models.ManyToManyField(
        "users.Student", through="StudentSessionAssociation"
    )
    mentors = models.ManyToManyField("users.Mentor", through="MentorSessionAssociation")

    isHappening = models.BooleanField(default=False)

    infrastructure_notes = models.TextField(
        default=None, help_text="Power, wifi, audio quality?", null=True, blank=True
    )
    mentorAdvisor_notes = models.TextField(default=None, null=True, blank=True)
    headmaster_notes = models.TextField(default=None, null=True, blank=True)
    teacher_notes = models.TextField(default=None, null=True, blank=True)
    parent_notes = models.TextField(default=None, null=True, blank=True)
    student_notes = models.TextField(default=None, null=True, blank=True)
    mentee_notes = models.TextField(default=None, null=True, blank=True)
    otherNotes = models.TextField(default=None, null=True, blank=True)
    # @varun we need to know which user can edit which fields

    agenda = models.TextField(default=None, null=True, blank=True)
    # figure out the ideal mentor mentee format and use of notion + journaling, if mentoring was a therapy intervetion, what are different formats? how does that play into the resources we are using?


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
    mentoring_notes = models.TextField(default=None, null=True, blank=True)
    # todo subject/class field and a computer field stating which computer the session is part of

    delay_notes = models.BooleanField(default=False)
    # warnings, risks, complexities etc. make this a type variable? issue_warning  need to figure out user workflow + story for session warning + communication @sarthak
    # if its easy for people to communicate over email or slack, there should be a simple way for mentors & mentees to communicate wether or not they are coming, the answer could be attendance, phones, parents, librian, idk but people should not need to wait
    # alert 30 minutes if mentee does not show, for mentors to leave, if problem repeats for 3 times in a row with power/internet/issues, then alert libraian and figure out a way to keep mentor engaged in the process
    # sarthak, we need to figure this out soon
    warnings = models.TextField(default=None, null=True, blank=True)
    issues = models.TextField(default=None, null=True, blank=True)
    feedback = models.TextField(default=None, null=True, blank=True)


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
    mentoring_notes = models.TextField(default=None, null=True, blank=True)
    # todo subject/class field and a computer field stating which computer the session is part of

    delay_notes = models.BooleanField(default=False)
    # warnings, risks, complexities etc. make this a type variable? issue_warning  need to figure out user workflow + story for session warning + communication @sarthak
    # if its easy for people to communicate over email or slack, there should be a simple way for mentors & mentees to communicate wether or not they are coming, the answer could be attendance, phones, parents, librian, idk but people should not need to wait
    # alert 30 minutes if mentee does not show, for mentors to leave, if problem repeats for 3 times in a row with power/internet/issues, then alert libraian and figure out a way to keep mentor engaged in the process
    # sarthak, we need to figure this out soon
    warnings = models.TextField(default=None, null=True, blank=True)
    issues = models.TextField(default=None, null=True, blank=True)
    feedback = models.TextField(default=None, null=True, blank=True)