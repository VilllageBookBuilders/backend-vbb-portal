from ast import NodeTransformer
from config.settings import test
import enum
from typing import BinaryIO

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from vbb_backend.utils.models.base import BaseUUIDModel
from vbb_backend.utils.models.question import QuestionareAnswers, QuestionareQuestions


class UserTypeEnum(enum.Enum):
    STUDENT = 100
    PARENT = 102 
    
    MENTOR = 200
    TEACHER = 300
    HEADMASTER = 400
    PROGRAM_DIRECTOR = 500 
    
    PROGRAM_MANAGER = 600    
    EXECUTIVE = 700


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
    
    # ? do users have default id??? or do we need to create such variable?
    user_created_date = models.DateField(blank=True, null=True)
    last_active_date = models.DateField(blank=True, null=True) #last time they logged on
    user_updated_date = models.DateField(blank=True, null=True) # last time information chaged
    user_renewal_date = models.DateField(blank=True, null=True) # when does their membership end and need to be vetted again

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=254, choices=LanguageChoices) #make this a choice of male, female, & other
    time_zone = models.CharField(max_length=32, choices=TIMEZONES)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=70, null=True, blank=True)
    state = models.CharField(max_length=70, null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    
    # figure out how do nickname ..> deidentification? like choose an avatar like a pokemon or something? sarthak talk with brett as he really wants this as investors/donors want deintentification
    
    primary_language = models.CharField(max_length=254, choices=LanguageChoices)
    secondary_language = models.CharField(max_length=254, choices=LanguageChoices)

    vbb_email = models.EmailField(
        null=True, unique=True, verbose_name=_("VBB Email"), help_text= "@villagementors.org"
    )
    phone_number = models.PhoneNumberField(blank=True, verbose_name=_("Phone Number"))
    avaibility_times = models.TextField(null=True, blank=True)
    user_bio = models.TextField(null=True, blank=True)

    notes = models.TextField(
        null=True, blank=True
    )  # Super User Specific

    def is_verified(self):
        return self.verification_level == self.VerificationLevelEnum.VERIFIED.value


# dynamic questions, surveying for questions that don't need to be embedded in a model, for later usage
class UserQuestionareQuestions(QuestionareQuestions):
    user_type = models.IntegerField(
        choices=UserTypeChoices, default=None, null=True, blank=True
    )
    # ? why are we doing this, sorry Just not understanding the benefit? questions vs answers? what how do we build low-code formso or just forms? what should the priority be @sarthak


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
    # ! need to improve based on: https://docs.google.com/spreadsheets/d/1ZCP85_1sKUPxYpXwjoMevV_zryJIfGYW_nMoG-M-56Y/edit#gid=734282936
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
    # ! delete since moved to user class? : address = models.TextField()
    personal_email = models.EmailField(
        null=True, unique=True, verbose_name=_("Personal Email")
    )
    isInterested = models.BooleanField(default=None, null=True)
    isIncomplete =  models.BooleanField(default=None, null=True)
    follow_up = models.BooleanField(default=None, null=True)
    # follow_up_dates = 
    # ? i don't understand  how do to arrays or lists
    occupation = models.CharField(
        max_length=70, null=True, blank=True, verbose_name=_("Occupation")
    )
    #if statement that only if college or high school student chapter is shown? should we do that?
    vbb_chapter = models.CharField(
        max_length=40, null=True, blank=True, verbose_name=_("VBB Chapter")
    )
    affiliation = models.CharField(
        max_length=70, null=True, blank=True, verbose_name=_("Affiliation")
    )
    isinCoporateEmployeeProgram = models.BooleanField(default=None, null=True) # will this be helpful or just do it based on emails? @sarthak
    referral_source = models.models.TextField(
        max_length=200, null=True, blank=True, verbose_name=_("Refferal")
    )
    isStaff = models.BooleanField(default=False, null=True)
    is_adult = models.BooleanField(default=None, null=True)
    terms_agreement = models.BooleanField(default=None, null=True)
    initials = models.CharField(max_length=6, null=True) #in place of signature
    mentor_application_video_link = models.URLField(max_length=200)
    application_submitted = models.BooleanField(default=None, null=True)
    #only mentor adviors or above chan verfiy application submission
    
    onetime_donated = models.BooleanField(default=None, null=True)
    recurring_donation = models.BooleanField(default=None, null=True)
    
    # legal_review_ = models.BooleanField(default=None, null=True)
    # todo make choices for legal review about submitted, ongoing, complex, done, good - talk with brett about this
    legal_notes_bymentor = models.TextField(null=True, blank=True)
    legal_notes_byreviewer = models.TextField(null=True, blank=True)
    vetted = models.BooleanField(default=None, null=True)
    trainingScheduled = models.BooleanField(default=None, null=True)
    attended_training = models.BooleanField(default=None, null=True)
    trainingNotes = models.TextField(null=True, blank=True)
    completed_trainingModules = models.BooleanField(default=None, null=True)
    nextLeadMentor_meeting_date = models.DateTimeField(null=True, blank=True)
    nextLeadMentor_meetingInfo = models.TextField(null=True, blank=True)
    leadmentor_notes = models.TextField(null=True, blank=True)
    metHeadmaster = models.BooleanField(default=None, null=True)
    headmaster_notes = models.TextField(null=True, blank=True)
    metMentorAdvisor = models.BooleanField(default=None, null=True)
    mentorAdvisor_notes = models.BooleanField(default=None, null=True)
    
    """
    Slot 
    Sessions <arraylist>
    Computer
    Program
    Note
    """
    additional_involvement = models.CharField(max_length=200, null=True, blank=True)
    
    #profile 
    #todo sarthak figure this out with brett
    """
    bio
    skills 
    interests
    education level
    whyMentoring
    psy testresutls
    research skills
    academic assemssemnt
    tech literacy
    engagement assement
    My favorite thing to do in my free time is _____
    When I grow up, I want to be ____
    Goals & Dreams Notes:
    Personal Struggles Notes:
    Other interests/hobbies:
    Skills Notes:
    Family Notes:
    Other Notes:
    """
    
    
    
class HeadMaster(BaseUUIDModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    
    # ! need to improve based on: https://docs.google.com/spreadsheets/d/1ZCP85_1sKUPxYpXwjoMevV_zryJIfGYW_nMoG-M-56Y/edit#gid=734282936

    # Further HeadMaster Information Here

# ! add teacher, add mentor advisor, add parent, add executive, add program director JUST a headmaster with more privilages, add village_learner 