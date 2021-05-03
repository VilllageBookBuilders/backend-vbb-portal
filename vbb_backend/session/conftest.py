import pytest
from pytest_factoryboy import register

from vbb_backend.session.tests.factories import *


register(SessionFactory)
register(StudentSessionAssociationFactory)
register(MentorSessionAssociationFactory)

register(SessionMentorStudentFactory)