import factory
from faker import Faker
from vbb_backend.users.models import User

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
        model = User

class ExecutiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class HeadmasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class ProgramManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class ProgramDirectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User