from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
import datetime
from uuid import uuid4
from vbb_backend.users.models import *
from vbb_backend.program.models import *
import datetime
import pytz
fake = Faker()
today = pytz.utc.localize(datetime.datetime.utcnow())
import psycopg2

class Command(BaseCommand):

    def genUser(self, user_type):
        fakeProfile = fake.simple_profile()
        new_user = User.objects.create(
            password='password',
            last_login=today,
            is_superuser=False,
            username=fakeProfile['username'],
            first_name=fakeProfile['name'].split()[0],
            last_name=fakeProfile['name'].split()[1],
            email=fake.email(),
            is_staff=True,
            is_active=True,
            date_joined=today,
            user_type=user_type,
            verification_level='1',
            vbb_chapter='vbbchapter',
            primary_language=fake.language_name(),
            time_zone=fake.timezone(),
            initials=fakeProfile['name'].split()[0][0] + fakeProfile['name'].split()[1][0],
            personal_email=fake.free_email(),
            phone=fake.phone_number(),
            occupation=fake.paragraph(nb_sentences=1),
            referral_source=fake.paragraph(nb_sentences=1),
            city=fake.city(),
            notes=fake.paragraph(nb_sentences=1),
            created_date=today,
            deleted=False,
            external_id=uuid4(),
            modified_date=today,
            date_of_birth=today
        )


        return 

    def genStudent(self, userId, classroom_id, school_level):
        Student.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            user_id=userId,
            classroom_id=classroom_id,
            school_level=school_level
        )

    def genProgram(self, program_director_id):
        Program.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            name=fake.city()+'  education program',
            time_zone=fake.timezone(),
            calendar_id=None,
            whatsapp_group=None,
            announcements_group=None,
            collaboration_group=None,
            village_info_link=None,
            default_language=fake.language_name(),
            program_director_id=program_director_id
        )
    def genSchool(self, program_id):
        lat,lon=fake.latlng()
        School.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            name=fake.company(),
            longitude=lon,
            latitude=lat,
            program_id=program_id
        )
    def genClassroom(self, school_id):
        Classroom.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            name=fake.company(),
            school_id=school_id
        )
    def genMentor(self, user_id):
        Mentor.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            user_id=user_id,
            address=fake.address(),
            affiliation=None,
            charged=None,
            desired_involvement=None,
            is_adult=None
        )


    def handle(self, *args, **options):
        # Connect to an existing database
        conn = psycopg2.connect("dbname=vbb user=postgres")

        # Open a cursor to perform database operations
        cur = conn.cursor()
        # Truncate DB
        Program.objects.all().delete()
        User.objects.all().delete()
        School.objects.all().delete()
        Classroom.objects.all().delete()
        Student.objects.all().delete()
        Mentor.objects.all().delete()
        #Restart Sequences
        cur.execute("ALTER SEQUENCE program_program_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE program_school_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE program_classroom_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE users_student_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE users_mentor_id_seq RESTART WITH 1")
        conn.commit()
        cur.close()
        conn.close()
        # #Insert user-headmaster
        for i in range(10):
            self.genUser(600)
        # Insert user-student
        for i in range(200):
            self.genUser(100)
        # Insert user-mentor
        for i in range(50):
            self.genUser(200)
        #Insert Program
        headmaster_id = User.objects.filter(user_type=600)[0].id
        self.genProgram(headmaster_id)
        #Insert school
        program_id = Program.objects.all()[0].id
        self.genSchool(program_id)
        #Insert Classroom
        school_id = School.objects.all()[0].id
        self.genClassroom(school_id)
        #Insert Students
        Croom = Classroom.objects.all()[0] #Classroom Objet
        students = User.objects.filter(user_type=100)
        for i in students:
            userId, classroom_id, school_id = i.id, Croom.id, Croom.school_id
            self.genStudent(userId, classroom_id, school_id)
        #Insert Mentors
        mentors = User.objects.filter(user_type=200)
        for i in mentors:
            self.genMentor(i.id)
            
        # pprint(user)
        # Commit changes to live DB
        # Close connection