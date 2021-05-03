import pytest
from pytest_factoryboy import register
from vbb_backend.program.tests.factories import *


register(ProgramFactory)
register(HeadmasterWithProgramFactory)
register(ManagerWithProgramFactory)
register(TeacherWithProgramFactory)
register(ComputerFactory)
register(MentorWithSlotFactory)
register(StudentWithSlotFactory)