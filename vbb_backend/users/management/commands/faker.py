from faker import Faker
from django.core.management.base import BaseCommand, CommandError
import psycopg2
# from polls.models import Question as Poll

class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        conn = psycopg2.connect("dbname=vbb user=postgres")
        cur = conn.cursor()
        fake = Faker()
        cur.execute("SELECT * FROM users_user;")
        print(cur.fetchone())
#         cur.execute("""
# ...     INSERT INTO some_table (an_int, a_date, a_string)
# ...     VALUES (%s, %s, %s);
# ...     """,
# ...     (10, datetime.date(2005, 11, 18), "O'Reilly"))
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
        cur.close()
        conn.close()