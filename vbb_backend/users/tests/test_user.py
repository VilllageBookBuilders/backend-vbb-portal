import pytest

from django.urls import reverse
from vbb_backend.users.models import User, UserTypeEnum
from django.db.utils import IntegrityError



@pytest.mark.django_db
def test_user_build(user_factory):
    newUser = user_factory.build()
    assert User.objects.count() == 0
    assert newUser.email ==  str(newUser)

@pytest.mark.django_db
def test_user_create(user_factory):
    newUser1 = user_factory.create()
    newUser2 = user_factory.create()
    assert User.objects.count() == 2

@pytest.mark.django_db
def test_user_fail_create(user_factory):
    with pytest.raises(IntegrityError): 
        user_factory.create(email=None)


@pytest.mark.django_db
def test_user_verification(user_factory):
    user = user_factory.create()
    assert User.objects.count() == 1
    assert user == User.objects.get(first_name = user.first_name)
    assert not user.is_verified() 
   