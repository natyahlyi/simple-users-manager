import os
import re
import names
import random
from django.core.management.base import BaseCommand
from django.conf import settings
import MySQLdb as db

from database.models import Users, Courses


SCRIPT_LOCATION = settings.BASE_DIR + "/database/script.sql"


class Command(BaseCommand):
    help = 'Creates all'

    def handle(self, *args, **options):
        # root Mysql user is used while db initialization,
        # so `DB_ROOT_PASSWORD` is needed in environment variables
        conn = db.connect(user="root", passwd=os.environ['DB_ROOT_PASSWORD'])

        with conn.cursor() as cursor:
            exec_sql_file(cursor, SCRIPT_LOCATION)
            create_users(cursor, 50)
            create_courses(cursor)

        conn.commit()
        conn.close()


def exec_sql_file(cursor, sql_file):
    print("\n[INFO] Executing SQL script file: '%s'" % (sql_file))
    statement = ""
    proc_flag = False
    procedure = ""
    for line in open(sql_file):
        if re.match(r'-- Procedure', line):
            proc_flag = True
            continue
        if re.match(r'-- End', line):
            # if settings.DEBUG:
            #     print("\n\n[DEBUG] Executing SQL statement:\n%s" % procedure)
            try:
                cursor.execute(procedure)
            except Exception as e:
                print("\n[WARN] MySQLError during execute"
                      " statement \n\tArgs: '%s'" % (str(e.args)))
            proc_flag = False
            procedure = ""
            continue

        if proc_flag:
            procedure += line
            continue

        if re.match(r'--', line):  # ignore sql comment lines
            continue

        # keep appending lines that don't end in ';'
        if not re.search(r'[^-;]+;', line):
            statement = statement + line
        # when you get a line ending in ';'
        #  then exec statement and reset for next statement
        else:
            statement = statement + line
            # if settings.DEBUG:
            #     print("[DEBUG] Executing SQL statement:\n%s" % statement)
            try:
                cursor.execute(statement)
            except Exception as e:
                print("\n[WARN] MySQLError during execute"
                      " statement \n\tArgs: '%s'" % (str(e.args)))

            statement = ""


def create_users(cursor, number):
    Users.cache_invalidate()
    operator_codes = ('093', '066', '073', '067')
    for n in range(number):
        name = names.get_full_name()
        f_name, l_name = name.split(' ')
        email = "{0}.{1}@mail.com".format(f_name.lower(), l_name.lower())
        status = random.choice(('Active', 'Inactive'))
        r_mobile = str(random.randint(1000000, 9999999))
        mobile = '+38' + random.choice(operator_codes) + r_mobile
        phone = '+380322' + str(random.randint(100000, 999999))
        cursor.callproc('create_user', [name, email, status, mobile, phone])


def create_courses(cursor):
    Courses.cache_invalidate()
    courses = (
        ('Python-Base', 'P012345'),
        ('Python-Database', 'P234566'),
        ('HTML', 'H345689'),
        ('Java-Base', 'J234266'),
        ('JavaScript-Base', 'JS234223'),
    )
    for title, code in courses:
        cursor.callproc('create_course', [title, code])
