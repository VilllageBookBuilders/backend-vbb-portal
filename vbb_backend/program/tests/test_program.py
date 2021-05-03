import pytest

@pytest.mark.django_db
def test_program_create(program_factory):
    newProgram1 = program_factory.create()
    newProgram2 = program_factory.create()
    assert Program.objects.count() == 2


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
   