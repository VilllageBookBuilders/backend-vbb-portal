import pytest
from pytest_factoryboy import register


from vbb_backend.users.tests.factories import *

# users module conftest.py

register(UserFactory)
register(ExecutiveFactory)
register(ParentFactory)