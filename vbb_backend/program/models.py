import enum
from datetime import datetime
from django.db import models
from django.db.models.base import Model
from rest_framework.exceptions import ValidationError

from vbb_backend.utils.models.base import BaseUUIDModel
from vbb_backend.users.models import UserTypeEnum

import pytz

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class LanguageEnum(enum.Enum):
    ENGLISH = "ENGLISH"


LanguageChoices = [(e.value, e.name) for e in LanguageEnum]


class Program(BaseUUIDModel):
    """
    This model represents a VBB village mentoring program

    Users that have foreign keys back to Program:
        ??? Program Director ???
        Student (through School)
    Teacher (through School)
        Mentor (through Slot)
        Mentor Advisor (many to many through a relation table)

    Models that have foreign keys back to Program:
        Slot (through Computer?)
        School
        Library
        Computer (?)
    """

    name = models.CharField(max_length=40, blank=False)
    time_zone = models.CharField(max_length=32, choices=TIMEZONES)
    calendar_id = models.CharField(max_length=254, null=True)
    whatsapp_group = models.CharField(max_length=254, null=True)
    announcements_group = models.CharField(max_length=254, null=True, blank=True)
    collaboration_group = models.CharField(max_length=254, null=True, blank=True)
    program_director = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True
    )
    village_info_link = models.CharField(max_length=200, null=True, blank=True)
    default_language = models.CharField(max_length=254, choices=LanguageChoices)

    ACCESS_CONTROL = {"program_director": [UserTypeEnum.ADVISOR.value]}

    @staticmethod
    def has_create_permission(request):
        return request.user.is_superuser

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_read_permission(request):
        return True  # User Queryset Filtering Here

    def has_object_write_permission(self, request):
        return request.user.is_superuser or request.user == self.program_director

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    def has_object_read_permission(self, request):
        return self.has_object_write_permission(request)


class School(BaseUUIDModel):  # LATER keep track of student attendance, and grades
    """
    This model represents a school in a village served by VBB.

    This model exists because one VBB Mentor Program draws students from multiple schools,
        but we would like to keep track (as much as possible) of which students are going
        to which schools in the village. This will facilitate our ultimate company goal
        to track and reduce school dropouts.

    Users associated to this school (through foreign keys):
        Headmaster(s)
        Students (through classrooms)
        Teachers (through classrooms)

    TODO: probably just remove/comment out school and classroom until we iron out our plans for working with schools
    """

    name = models.CharField(max_length=40, blank=False)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    # link to 3rd party LMS ?
    # has studens (students have foreign keys back to school)
    # has a headmaster (usually the same as program director) ("has" means these things have foreign keys back to school)
    # has classrooms ("has" means these things have foreign keys back to school)
    # has teachers and students ("has" means these things have foreign keys back to school)

    @staticmethod
    def has_create_permission(request):
        program = Program.objects.get(
            external_id=request.parser_context["kwargs"]["program_external_id"]
        )
        return request.user.is_superuser or request.user == program.program_director

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_read_permission(request):
        return True  # User Queryset Filtering Here

    def has_object_write_permission(self, request):
        return (
            request.user.is_superuser or request.user == self.program.program_director
        )

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    def has_object_read_permission(self, request):
        return self.has_object_write_permission(request)


class Classroom(BaseUUIDModel):  # DEPRECATED
    """
    This model is a basic representation of a classroom in the schools that VBB serves.

    Each school has at least one classroom, including "default", "dropped out", and "graduated"

    Users associated with each classroom (through foreign keys):
        Student(s)
        Teacher(s?)

    TODO: is it possible for a teacher or student to be associated with multiple classrooms or even multiple schools?
    """

    name = models.CharField(max_length=40, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)

    @staticmethod
    def has_create_permission(request):
        school = School.objects.get(
            external_id=request.parser_context["kwargs"]["school_external_id"]
        )
        return (
            request.user.is_superuser or request.user == school.program.program_director
        )

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_read_permission(request):
        return True  # User Queryset Filtering Here

    def has_object_write_permission(self, request):
        return (
            request.user.is_superuser
            or request.user == self.school.program.program_director
        )

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    def has_object_read_permission(self, request):
        return self.has_object_write_permission(request)


class Library(BaseUUIDModel):
    """
    This Model represents a Library in a Village Book Builders Program.
    Not all VBB Programs currently have libraries
    Basically, a library has books and people who can checkout bookss
    TODO figure out if we should integrate a third party library management system
    """

    name = models.CharField(max_length=40, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name


class Book(BaseUUIDModel):
    """
    This Model Represents a book that can be checked out from a VBB Library
        title: the title of the book
        isbn: the 13 digit identifying barcode on the back of the book (TODO: may need to adjustthis to allow for ISBN-9)
        library: the library the book belongs to
        reading_level: the grade level this book is associated with (ie 0 is kindergarten, 12 is 12th grade level, etc)
        is_available: set to true when the book is not lended to anyone and is available at the library
    """

    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=40, null=True, blank=True)
    isbn = models.IntegerField(null=True, blank=True)
    reading_level = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)


class Checkout(BaseUUIDModel):
    """
    This model represents a checkout instance to keep track of who has checked out books at a village library and when
    """

    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    extension_date = models.DateTimeField(null=True, blank=True)
    has_returned = models.BooleanField(default=False)


class Computer(BaseUUIDModel):
    """
    This Model Represents a Computer in a VBB Mentor Program that can host mentoring slots
    """

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
    )
    computer_number = models.IntegerField(null=True)
    computer_email = models.EmailField(max_length=70, null=True)
    room_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return (
            f"{str(self.program)} {str(self.computer_number)} + ({self.computer_email})"
        )

    @staticmethod
    def has_create_permission(request):
        program = Program.objects.get(
            external_id=request.parser_context["kwargs"]["program_external_id"]
        )
        return request.user.is_superuser or request.user == program.program_director

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_read_permission(request):
        return True  # User Queryset Filtering Here

    def has_object_write_permission(self, request):
        return (
            request.user.is_superuser or request.user == self.program.program_director
        )

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    def has_object_read_permission(self, request):
        return self.has_object_write_permission(request)


class Slot(BaseUUIDModel):
    """
    This Model Represents a slot that the mentor program decides to have with one of its computers,
    **eg , a slot can be for a Computer A for firday 10AM to friday 12AM**
    The slot is not editable, once the slot is to be updated the model object has to be deleted and recreated
    The slot object has no starting time or ending time, slots made are run throughout the year, to cancel a slot the slot has to be deleted
    The slot can be of any duration less than 24 hours

    the slot start and end refer to the start and end of a session in the slot,
    we are only concerned with the day of the week and the time , so month and year does not make a difference

    the slot will be assigned to a mentor, which connects the mentor app and the program app
    """

    # Default Min date not used as this can cause issues in some databases and systems
    DEAFULT_INIT_DATE = datetime.fromisoformat(
        "2000-01-03 00:00:00"
    )  # First Monday of the year 2000
    # DO NOT CHANGE THE DEFAULT INIT DATE | USED FOR EASE OF USE

    computer = models.ForeignKey(
        Computer,
        on_delete=models.PROTECT,
        null=True,
    )
    language = models.CharField(max_length=254, choices=LanguageChoices)
    schedule_start = models.DateTimeField(
        null=False, blank=False
    )  # All Date Times in UTC
    schedule_end = models.DateTimeField(
        null=False, blank=False
    )  # All Date Times are in UTC
    start_date = models.DateField(auto_now=True)  # When the slot becomes active
    end_date = models.DateField(null=True, blank=True)  # if and when the slot ends
    event_id = models.CharField(max_length=60, null=True, blank=True)
    hangouts_link = models.CharField(max_length=60, null=True, blank=True)
    max_students = models.IntegerField(default=1)
    assigned_students = models.IntegerField(
        default=0
    )  # Storing to avoid recalculation each time
    is_mentor_assigned = models.BooleanField(default=False)
    is_student_assigned = models.BooleanField(default=False)

    students = models.ManyToManyField("users.Student", through="StudentSlotAssociation")
    mentors = models.ManyToManyField("users.Mentor", through="MentorSlotAssociation")

    def save(self, *args, **kwargs):

        if Slot.objects.filter(
            computer=self.computer,
            schedule_end__gt=self.schedule_start,
            schedule_start__lt=self.schedule_end,
        ).exists():
            raise ValidationError({"schedule": "Conflict Found"})

        return super().save(*args, **kwargs)

    def start_day_of_the_week(self):
        return self.schedule_start.date().weekday()

    def end_day_of_the_week(self):
        return self.schedule_end.date().weekday()

    def start_hour(self):
        return self.schedule_start.hour

    def end_hour(self):
        return self.schedule_end.hour

    def start_minute(self):
        return self.schedule_start.minute

    def end_minute(self):
        return self.schedule_end.minute

    @staticmethod
    def has_create_permission(request):
        computer = Computer.objects.get(
            external_id=request.parser_context["kwargs"]["computer_external_id"]
        )
        return (
            request.user.is_superuser
            or request.user == computer.program.program_director
        )

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_read_permission(request):
        return True  # User Queryset Filtering Here

    def has_object_write_permission(self, request):
        return (
            request.user.is_superuser
            or request.user == self.computer.program.program_director
        )

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    def has_object_read_permission(self, request):
        return self.has_object_write_permission(request)


class StudentSlotAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Slot Object
    """

    student = models.ForeignKey(
        "users.Student",
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_slot",
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.SET_NULL, null=True, related_name="slot_student"
    )
    priority = models.IntegerField(default=0)  # 0 is the highest priority

    @staticmethod
    def has_create_permission(request):
        program = Program.objects.get(
            external_id=request.parser_context["kwargs"]["program_external_id"]
        )
        return request.user.is_superuser or request.user == program.program_director

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_read_permission(request):
        return True  # User Queryset Filtering Here

    def has_object_write_permission(self, request):
        return (
            request.user.is_superuser
            or request.user == self.slot.computer.program.program_director
        )

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    def has_object_read_permission(self, request):
        return self.has_object_write_permission(request)


class MentorSlotAssociation(BaseUUIDModel):
    """
    This connects the student user object with a Slot Object
    """

    mentor = models.ForeignKey(
        "users.Mentor", on_delete=models.SET_NULL, null=True, related_name="mentor_slot"
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.SET_NULL, null=True, related_name="slot_mentor"
    )
    priority = models.IntegerField(default=0)  # 0 is the highest priority
    is_confirmed = models.BooleanField(default=False) # This is only editable by the program director or above