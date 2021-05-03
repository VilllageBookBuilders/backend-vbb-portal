import factory
from faker import Faker
import factory
from vbb_backend.users.models import *

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda a : "{}.{}@villagebookbuilders.org".format(a.first_name, a.last_name))
    password = "password"

class MentorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mentor

class ExecutiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Executive


class HeadmasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Headmaster


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

class ProgramManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramManager

class ProgramDirectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramDirector