from faker import Faker
from django.core.management.base import BaseCommand, CommandError
import psycopg2
from django.core.serializers.json import DjangoJSONEncoder
import pprint
import datetime
import random
import uuid

def genHeadmaster():
    fake = Faker()
    today = datetime.datetime.today()
    fakeProfile = fake.simple_profile()
    pprint.pprint(fake.phone_number())

    return (
        # random.randint(10, 1000),
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
        '600',
        '1',
        'vbbchapter',
        fake.language_name(),
        fake.timezone(),
        'A J',
        fake.free_email(),
        fake.phone_number()[3:9],
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

pprint.pprint(genHeadmaster())

class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        conn = psycopg2.connect("dbname=vbb user=postgres")
        cur = conn.cursor()
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
        [genHeadmaster() for i in range(10)])
        cur.execute("SELECT * FROM users_user;")
        pprint.pprint(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()