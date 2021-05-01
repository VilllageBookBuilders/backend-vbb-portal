import pytest

from vbb_backend.users.models import User
from vbb_backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user_factory() -> UserFactory:
    return UserFactory


