import enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from vbb_backend.otherIntegrations.mailChimp.mailChimp import subscribe_newsletter
from phonenumber_field.modelfields import PhoneNumberField

from vbb_backend.utils.models.base import BaseUUIDModel
from vbb_backend.utils.models.question import QuestionareAnswers, QuestionareQuestions


class UserTypeEnum(enum.Enum):
    STUDENT = 100
    MENTOR = 200
    TEACHER = 300
    DIRECTOR = 400
    ADVISOR = 500
    HEADMASTER = 600


UserTypeChoices = [(e.value, e.name) for e in UserTypeEnum]

from vbb_backend.program.models import School, LanguageChoices, TIMEZONES


class User(AbstractUser, BaseUUIDModel):
    """Default user for Village Book Builders Backend.
    The AbstractUser Model already includes most of the required fields for a User.
    The Extra fields are used to store details of a user in VBB
    """

    class VerificationLevelEnum(enum.Enum):
        # WE can define what each Level Means and so on or default to VERIFIED
        LEVEL1 = 1
        LEVEL2 = 2
        VERIFIED = 100

    VerificationLevelChoices = [(e.value, e.name) for e in VerificationLevelEnum]

    user_type = models.IntegerField(
        choices=UserTypeChoices, default=UserTypeEnum.MENTOR.value
    )

    verification_level = models.IntegerField(
        choices=VerificationLevelChoices, default=VerificationLevelEnum.LEVEL1.value
    )

    vbb_chapter = models.CharField(
        max_length=40, null=True, blank=True, verbose_name=_("VBB Chapter")
    )
    date_of_birth = models.DateField(blank=True, null=True)
    primary_language = models.CharField(max_length=254, choices=LanguageChoices)
    time_zone = models.CharField(max_length=32, choices=TIMEZONES)

    initials = models.CharField(max_length=6, null=True)
    personal_email = models.EmailField(
        null=True, unique=True, verbose_name=_("Personal Email")
    )

    phone = PhoneNumberField(blank=True, verbose_name=_("Phone Number"))
    occupation = models.CharField(
        max_length=70, null=True, blank=True, verbose_name=_("Occupation")
    )

    referral_source = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("Refferal")
    )

    city = models.CharField(max_length=70, null=True, blank=True)
    notes = models.TextField(
        max_length=512, null=True, blank=True
    )  # Super User Specific

    def is_verified(self):
        return self.verification_level == self.VerificationLevelEnum.VERIFIED.value


# dynamic questions, surveying for questions that don't need to be embedded in a model, for later usage
class UserQuestionareQuestions(QuestionareQuestions):
    user_type = models.IntegerField(
        choices=UserTypeChoices, default=None, null=True, blank=True
    )


class UserQuestionareAnswers(QuestionareAnswers):
    question = models.ForeignKey(
        UserQuestionareQuestions,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )


class Student(BaseUUIDModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    # change to school
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    school_level = models.IntegerField()  # -1 for graduated , -2 for dropout
    group_name = models.CharField(max_length=256)

    # add models to this.

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

    # Further Student Information Here


class Mentor(BaseUUIDModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    # Further Mentor Information Here
    charged = models.TextField(max_length=1024, null=True)
    address = models.TextField()
    desired_involvement = models.CharField(max_length=200, null=True, blank=True)
    affiliation = models.CharField(
        max_length=70, null=True, blank=True, verbose_name=_("Affiliation")
    )
    is_adult = models.BooleanField(default=None, null=True)


class HeadMaster(BaseUUIDModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    # Further HeadMaster Information Here


class SubscriptionTypeEnum(enum.Enum):
    REGISTRATION = "REGISTRATION"
    VBB_NEWSLETTER = "VBB_NEWSLETTER"


SubscriptionTypeChoices = [(e.value, e.name) for e in SubscriptionTypeEnum]


class NewsletterSubscriber(BaseUUIDModel):
    """
    Model to store information about Newsletter Subscriptions
    """

    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, verbose_name=_("Phone Number"))
    email = models.EmailField(
        null=False, blank=False, unique=True, verbose_name=_("Email")
    )
    subscriber_type = models.CharField(
        max_length=254,
        choices=SubscriptionTypeChoices,
        default=SubscriptionTypeEnum.VBB_NEWSLETTER.value,
    )

    def save(self, **kwargs) -> None:
        data = {
            "email": self.email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": self.first_name,
                "LNAME": self.last_name,
            },
        }
        subscribe_newsletter(data)
        return super().save(**kwargs)