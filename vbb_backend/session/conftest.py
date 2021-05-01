import pytest

from vbb_backend.session.models import Session
from vbb_backend.session.tests.factories import SessionFactory


@pytest.fixture
def session_factory() -> SessionFactory:
    return SessionFactory


