import pytest

from pytest_factoryboy import register

from vbb_backend.program.tests.factories import SlotFactory, ComputerFactory
from vbb_backend.users.tests.factories import *
"""
This conf file is used by all modules. Only add fixtures
that span multiple modules.
"""
@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath

register(SlotFactory)
register(ComputerFactory)


register(MentorFactory)
register(StudentFactory)
register(TeacherFactory)
register(HeadmasterFactory)
register(ProgramManagerFactory)
register(ProgramDirectorFactory)