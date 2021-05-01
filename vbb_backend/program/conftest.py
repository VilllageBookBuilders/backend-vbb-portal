import pytest

from vbb_backend.program.models import Program
from vbb_backend.program.tests.factories import ProgramFactory



@pytest.fixture
def program_factory() -> ProgramFactory:
    return ProgramFactory


