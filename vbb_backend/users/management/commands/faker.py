from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
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

def calcPerc(total, current):
    return 0 if current == 0 else (current*100)//total

def verbose(*args, end='\n'):
    if (True):
        for i in args:
            print(i, end=end)
# Script Variables

NUM_OF_HEADMASTERS_AND_PROGRAMS_AND_SCHOOLS = 1
NUM_OF_MENTORS = NUM_OF_HEADMASTERS_AND_PROGRAMS_AND_SCHOOLS * 12
NUM_OF_CLASSROOMS = NUM_OF_HEADMASTERS_AND_PROGRAMS_AND_SCHOOLS * 3
NUM_OF_STUDENTS = NUM_OF_CLASSROOMS * 25
class Command(BaseCommand):
    #This function generates and inserts Users into db
    def genUser(self, user_type, amount=1):
        fn = fake.first_name()
        ln = fake.last_name()
        new_user = User(
            password='password',
            last_login=today,
            is_superuser=False,
            username= fn + ln + str(fake.random_int()),
            first_name= fn,
            last_name= ln,
            email= fake.email(),
            is_staff=True,
            is_active=True,
            date_joined=today,
            user_type=user_type,
            verification_level='1',
            vbb_chapter='vbbchapter' + fake.word(),
            primary_language=fake.language_name(),
            time_zone=fake.timezone(),
            initials=fn[0] + ln[0],
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

        new_user.set_password('password')
        new_user.save()
        return new_user

    #This function generates and inserts Students into db
    def genStudent(self, data):
        userId, classroom_id = data
        Student.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            user_id=userId,
            classroom_id=classroom_id,
            school_level=fake.random_int(0, 100)
        )
    #This function generates and inserts the program into db
    def genProgram(self, program_director_id):
        new_prog = Program.objects.create(
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
        return f'ProgId: {new_prog.id}, Director: {new_prog.program_director_id}'
    #This function generates and inserts school into db
    def genSchool(self, program_id):
        lat,lon=fake.latlng()
        new_school = School.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            name=fake.company(),
            longitude=lon,
            latitude=lat,
            program_id=program_id
        )
        return f'SchoolId: {new_school.id}, Program: {new_school.program_id}'
    #This function generates and inserts classroom into db
    def genClassroom(self, school_id):
        new_classroom = Classroom.objects.create(
            created_date=today,
            modified_date=today,
            deleted=False,
            external_id=uuid4(),
            name=fake.company(),
            school_id=school_id
        )
        return f'ClassroomId: {new_classroom.id}, SchoolId: {new_classroom.school_id}'
    #This function generates and inserts Mentoors into db
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
    
    def exceptionHandlingLoop(self, callback, amount, paramForCallback=None):
            toGenerate, IntE, DataE, UniqE, operations,totalErrors = 0,0,0,0,0,0
            print(f"Executing {callback.__name__}")
            while toGenerate < amount:
                try:
                    operations+=1
                    if (type(paramForCallback) is list):
                        # This next line is here just to handle the special case when the string has only one item inside
                        rand_choice = paramForCallback.pop(fake.random_int(0, len(paramForCallback)-1)) if len(paramForCallback) > 1 else paramForCallback[0]
                        result = callback(rand_choice)
                    elif (paramForCallback):
                        result = callback(paramForCallback)
                    else:
                        callback()
                except IntegrityError as exc:
                    IntE+=1 #Counter for Integrity errors
                    totalErrors+=1 #Counter for all errors

                except Exception as exc:
                    ExcName = exc.__class__.__name__
                    totalErrors+=1 #Counter for all errors
                    if (ExcName == 'UniquenessException'):
                        UniqE+=1 #Counter for Uniqueness excep error
                    elif (ExcName == 'DataError'):
                        DataE+=1 #Counter for DataErrors
                    else:
                        raise exc
                else:
                    toGenerate+=1
                    Exec = f"Executing {callback.__name__} #{operations:,} | {calcPerc(amount,toGenerate)}% | "
                    IntegrityString = f"IntegrityError: {IntE:,} {calcPerc(operations, IntE)}%  "
                    UniqueString = f"UniquenessException: {UniqE:,} {calcPerc(operations, UniqE)}%  "
                    dataErrString = f"DataError: {DataE:,} {calcPerc(operations, DataE)}%  "
                    errRateString = f"Total Errors: {totalErrors:,} {calcPerc(operations, totalErrors)}%"
                    verbose(Exec + IntegrityString + UniqueString + dataErrString + errRateString)
            ExecFinStr = f"\n\tExecuted {callback.__name__} {toGenerate:,} times successfully, with total of {operations:,} operations"
            IntFinString = f"\n\tIntegrityError: {IntE:,} | {calcPerc(operations, IntE)}% of operations"
            UniqFinString = f"\n\tUniquenessException: {UniqE:,} | {calcPerc(operations, UniqE)}% of operations"
            DataErrFinString = f"\n\tDataError: {DataE:,} | {calcPerc(operations, DataE)}% of operations"
            ErrRateFinString = f"\n\tTotal Errors: {totalErrors:,} {calcPerc(operations, totalErrors)}% of operations\n"
            verbose(ExecFinStr + IntFinString + UniqFinString + DataErrFinString + ErrRateFinString)
            print(f"Done with {callback.__name__}")

    def hardResetdb(self):
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
        #Restart Sequences could not find a Django oriented solution to this also it is not necesary is for ease of use
        cur.execute("ALTER SEQUENCE program_program_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE program_school_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE program_classroom_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE users_student_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE users_mentor_id_seq RESTART WITH 1")
        conn.commit()
        cur.close()
        conn.close()

    def softResetdb(self):
        # Truncate DB
        p =  Program.objects.all()
        for i in p:
            i.deleted = True
        Program.objects.bulk_update(p, ['deleted'])\

        u = User.objects.all()
        for i in u:
            i.deleted = True
        User.objects.bulk_update(u, ['deleted'])

        s = School.objects.all()
        for i in s:
            i.deleted = True
        School.objects.bulk_update(s, ['deleted'])

        c = Classroom.objects.all()
        for i in c:
            i.deleted = True
        Classroom.objects.bulk_update(c, ['deleted'])

        stu = Student.objects.all()
        for i in stu:
            i.deleted = True
        Student.objects.bulk_update(stu, ['deleted'])

        m = Mentor.objects.all()
        for i in m:
            i.deleted = True
        Mentor.objects.bulk_update(m, ['deleted'])
    
    def handle(self, *args, **options):
        self.hardResetdb()
        # self.softResetdb()
        # Insert user-headmaster
        self.exceptionHandlingLoop(self.genUser, NUM_OF_HEADMASTERS_AND_PROGRAMS_AND_SCHOOLS, 600)
        # # Insert user-student
        self.exceptionHandlingLoop(self.genUser, NUM_OF_STUDENTS, 100)
        # Insert user-mentor
        self.exceptionHandlingLoop(self.genUser, NUM_OF_MENTORS, 200)
        # #Insert Program per headmaster
        headmasters = [hm.id for hm in User.objects.filter(user_type=600).exclude(deleted=True)] #Headmasters Id's
        self.exceptionHandlingLoop(self.genProgram, NUM_OF_HEADMASTERS_AND_PROGRAMS_AND_SCHOOLS, headmasters)
        
        #Insert school
        programs = [prg.id for prg in Program.objects.all().exclude(deleted=True)]
        self.exceptionHandlingLoop(self.genSchool, NUM_OF_HEADMASTERS_AND_PROGRAMS_AND_SCHOOLS, programs)
        #Insert Classroom
        Schools = [ school.id for school in School.objects.all().exclude(deleted=True)] # List of school Id's
        self.exceptionHandlingLoop(self.genClassroom, NUM_OF_CLASSROOMS, fake.random_elements(Schools, length=NUM_OF_CLASSROOMS))

        #Insert Students
        Classrooms = [cls.id for cls in Classroom.objects.all().exclude(deleted=True)] #Classrooms id's
        students = [std.id for std in User.objects.filter(user_type=100).exclude(deleted=True)]
        studentAndClassroomPairings = [ (stdId, fake.random_element(Classrooms)) for stdId in students]
        self.exceptionHandlingLoop(self.genStudent, NUM_OF_STUDENTS, studentAndClassroomPairings)
        # Insert Mentors
        mentors = [ mnt.id for mnt in User.objects.filter(user_type=200).exclude(deleted=True)]# Mentor Id's
        self.exceptionHandlingLoop(self.genMentor, NUM_OF_MENTORS, mentors)

        print('Done')
