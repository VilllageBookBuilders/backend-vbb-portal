import pytest

from vbb_backend.session.models import Session


@pytest.mark.django_db
def test_session_create(session_factory):
    newSession1 = session_factory.create()
    newSession2 = session_factory.create()
    assert Session.objects.count() == 2

# @pytest.mark.django_db
# def test_session_build(session_mentor_student_factory):
#     newSessionMentorStudent = session_mentor_student_factory.create()
#     assert  newSessionMentorStudent  == 42

# @pytest.mark.django_db
# def test_session_fail_create(session_factory):
#     with pytest.raises(IntegrityError): 
#         session_factory.create(email=None)


# @pytest.mark.django_db
# def test_session_verification(session_factory):
#     session = session_factory.create()
#     assert Session.objects.count() == 1
#     assert session == Session.objects.get(first_name = session.first_name)
#     assert not session.is_verified() 
   