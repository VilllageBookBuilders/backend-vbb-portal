import factory

from vbb_backend.session.models import *
from vbb_backend.program.tests.factories import *



class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Session

    slot = factory.SubFactory(SlotFactory)
    computer = factory.SubFactory(ComputerFactory)
    start = factory.Faker("time")
    end =   factory.Faker("time")


  
class StudentSessionAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentSessionAssociation
    student = factory.SubFactory(StudentFactory)
    session = factory.SubFactory(SessionFactory)
   

class MentorSessionAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MentorSessionAssociation
    mentor = factory.SubFactory(MentorFactory)
    session = factory.SubFactory(SessionFactory)

class SessionMentorStudentFactory(MentorSessionAssociationFactory, StudentSessionAssociationFactory):
    mentor_session = factory.RelatedFactory(
        MentorSessionAssociationFactory,
        factory_related_name='session',
    )
    student_session = factory.RelatedFactory(
        StudentSessionAssociationFactory,
        factory_related_name='session',
    )