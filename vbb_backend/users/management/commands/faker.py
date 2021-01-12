from faker import Faker
from django.core.management.base import BaseCommand, CommandError
import psycopg2
from django.core.serializers.json import DjangoJSONEncoder
import pprint
import datetime
import random
import uuid
fake = Faker()
today = datetime.datetime.today()


class Command(BaseCommand):
    def genUser(self, user_type):
        # print('generated user')
        fakeProfile = fake.simple_profile()
        return (
            'password',
            today,
            'FALSE',
            fakeProfile['username'],
            fakeProfile['name'].split()[0],
            fakeProfile['name'].split()[1],
            fake.email(),
            'TRUE',
            'TRUE',
            today,
            user_type,
            '1',
            'vbbchapter',
            fake.language_name(),
            fake.timezone(),
            fakeProfile['name'].split()[0][0] + fakeProfile['name'].split()[1][0],
            fake.free_email(),
            fake.phone_number(),
            fake.paragraph(nb_sentences=1),
            fake.paragraph(nb_sentences=1),
            fake.city(),
            fake.paragraph(nb_sentences=1),
            today,
            'FALSE',
            uuid.uuid4(),
            today,
            today
        )

    def addStudent(self, userId, cursor):
        return (
            today,
            today,
            'FALSE',
            uuid.uuid4(),
            userId,
            1,
            2
        )

    def addHeadmaster(self, userId):
        return (
            today,
            today,
            'FALSE',
            uuid.uuid4(),
            userId
        )
    def handle(self, *args, **options):
        # Open conection
        conn = psycopg2.connect("dbname=vbb user=postgres")
        cur = conn.cursor()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        hm_from, hm_to = 1, 11
        std_from, std_to = 11,211

        
        if True:
            tables = [
                'users_user',
                'users_headmaster'
            ]
            for i in tables:
                cur.execute('TRUNCATE TABLE %s CASCADE;', [i])
                cur.execute('ALTER SEQUENCE %s_id_seq  RESTART WITH 1', [i])

        # Insert 10 Headmasters
        psycopg2.extras.execute_values(cur,
        """INSERT INTO users_user (
        password,	
        last_login,	
        is_superuser,	
        username,	
        first_name,	
        last_name,	
        email,	
        is_staff,	
        is_active,	
        date_joined,	
        user_type,	
        verification_level,	
        vbb_chapter,	
        primary_language,	
        time_zone,	
        initials,	
        personal_email,	
        phone,	
        occupation,	
        referral_source,	
        city,	
        notes,	
        created_date,	
        deleted,	
        external_id,	
        modified_date,	
        date_of_birth
        ) VALUES %s
        """,
        [self.genUser(600) for i in range(hm_from, hm_to)])
        conn.commit()

        psycopg2.extras.execute_values(cur,
        """INSERT INTO users_headmaster (
        created_date,
        modified_date,
        deleted,
        external_id,
        user_id
        ) VALUES %s
        """,
        [self.addHeadmaster(i) for i in range(hm_from, hm_to)])
        # conn.commit()
        # Insert 200 Students

        # psycopg2.extras.execute_values(cur,
        # """INSERT INTO users_user (
        # password,	
        # last_login,	
        # is_superuser,	
        # username,	
        # first_name,	
        # last_name,	
        # email,	
        # is_staff,	
        # is_active,	
        # date_joined,	
        # user_type,	
        # verification_level,	
        # vbb_chapter,	
        # primary_language,	
        # time_zone,	
        # initials,	
        # personal_email,	
        # phone,	
        # occupation,	
        # referral_source,	
        # city,	
        # notes,	
        # created_date,	
        # deleted,	
        # external_id,	
        # modified_date,	
        # date_of_birth
        # ) VALUES %s
        # """,
        # [self.genUser(200) for i in range(10,200)])

        # psycopg2.extras.execute_values(cur,
        # """INSERT INTO users_student (
        # created_date,
        # modified_date,
        # deleted,
        # external_id,
        # user_id,
        # classroom_id,
        # school_level
        # ) VALUES %s
        # """,
        # [self.genStudent(i, dict_cur) for i in range(12,13)])


        # Commit changes to live DB
        conn.commit()
        # Close connection
        cur.close()
        conn.close()