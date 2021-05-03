import factory

from vbb_backend.program.models import *

from vbb_backend.users.tests.factories import *


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program

    name = factory.Faker("name")
    program_director = factory.SubFactory(ProgramDirectorFactory)
 
    # @staticmethod
    # def has_create_permission(request):
    #     return request.user.is_superuser

    # @staticmethod
    # def has_write_permission(request):
    #     return True

    # @staticmethod
    # def has_read_permission(request):
    #     return True  # User Queryset Filtering Here

    # def has_object_write_permission(self, request):
    #     return request.user.is_superuser or request.user == self.program_director

    # def has_object_update_permission(self, request):
    #     return self.has_object_write_permission(request)

    # def has_object_read_permission(self, request):
    #     return self.has_object_write_permission(request)


class HeadmastersProgramAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HeadmastersProgramAssociation

    headmaster = factory.SubFactory(HeadmasterFactory)
    program = factory.SubFactory(ProgramFactory)


class HeadmasterWithProgramFactory(HeadmastersProgramAssociationFactory):
    headmaster_with_program = factory.RelatedFactory(
        HeadmastersProgramAssociationFactory,
        factory_related_name="program_headmaster",
    )


class TeachersProgramAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TeachersProgramAssociation
        
    teacher = factory.SubFactory(TeacherFactory)
    program = factory.SubFactory(ProgramFactory)


class TeacherWithProgramFactory(TeachersProgramAssociationFactory):
    teacher_with_program = factory.RelatedFactory(
        TeachersProgramAssociationFactory,
        factory_related_name="program_teacher",
    )


class ManagersProgramAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ManagersProgramAssociation
        
    program_manager = factory.SubFactory(ProgramManagerFactory)
    program = factory.SubFactory(ProgramFactory)


class ManagerWithProgramFactory(ManagersProgramAssociationFactory):
    manager_with_program = factory.RelatedFactory(
        ManagersProgramAssociationFactory,
        related_name="program_manager"
    )


class ComputerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Computer
    program = factory.SubFactory(ProgramFactory)


class SlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Slot
    computer = factory.SubFactory(ComputerFactory)
    # def save(self, *args, **kwargs):

    #     if Slot.objects.filter(
    #         computer=self.computer,
    #         schedule_end__gt=self.schedule_start,
    #         schedule_start__lt=self.schedule_end,
    #     ).exists():
    #         raise ValidationError({"schedule": "Conflict Found"})

    #     return super().save(*args, **kwargs)

    # def start_day_of_the_week(self):
    #     return self.schedule_start.date().weekday()

    # def end_day_of_the_week(self):
    #     return self.schedule_end.date().weekday()

    # def start_hour(self):
    #     return self.schedule_start.hour

    # def end_hour(self):
    #     return self.schedule_end.hour

    # def start_minute(self):
    #     return self.schedule_start.minute

    # def end_minute(self):
    #     return self.schedule_end.minute

    # @staticmethod
    # def has_create_permission(request):
    #     computer = Computer.objects.get(external_id=request.parser_context["kwargs"]["computer_external_id"])
    #     return request.user.is_superuser or request.user == computer.program.program_director

    # @staticmethod
    # def has_write_permission(request):
    #     return True

    # @staticmethod
    # def has_read_permission(request):
    #     return True  # User Queryset Filtering Here

    # def has_object_write_permission(self, request):
    #     return request.user.is_superuser or request.user == self.computer.program.program_director

    # def has_object_update_permission(self, request):
    #     return self.has_object_write_permission(request)

    # def has_object_read_permission(self, request):
    #     return self.has_object_write_permission(request)


class StudentSlotAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentSlotAssociation

    student = factory.SubFactory(StudentFactory)
    slot = factory.SubFactory(SlotFactory)

    # @staticmethod
    # def has_create_permission(request):
    #     program = Program.objects.get(external_id=request.parser_context["kwargs"]["program_external_id"])
    #     return request.user.is_superuser or request.user == program.program_director

    # @staticmethod
    # def has_write_permission(request):
    #     return True

    # @staticmethod
    # def has_read_permission(request):
    #     return True  # User Queryset Filtering Here

    # def has_object_write_permission(self, request):
    #     return request.user.is_superuser or request.user == self.slot.computer.program.program_director

    # def has_object_update_permission(self, request):
    #     return self.has_object_write_permission(request)

    # def has_object_read_permission(self, request):
    #     return self.has_object_write_permission(request)


class StudentWithSlotFactory(StudentSlotAssociationFactory):
    student_slot = factory.RelatedFactory(
        StudentSlotAssociationFactory,
        related_name="student_slot"
    )


class MentorSlotAssociationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MentorSlotAssociation

    mentor = factory.SubFactory(MentorFactory)
    slot = factory.SubFactory(SlotFactory)
 

class MentorWithSlotFactory(MentorSlotAssociationFactory):
    mentor_slot = factory.RelatedFactory(
        MentorSlotAssociationFactory,
        related_name="mentor_slot"
    )
