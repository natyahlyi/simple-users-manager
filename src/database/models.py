from django.db import connection

# for simple caching, uses django cache backend
from memoize import memoize, delete_memoized

from collections import namedtuple

# Container for 'course' instance
Course = namedtuple('Course', ('id', 'title', 'code'))


class User:
    """
    Container for: creating, updating and storing 'user' instance
    """
    def __init__(self, u_id=None, name=None, email=None,
                 status="Inactive", mobile='', phone='',
                 update=False, enroll=None):
        self.name = name
        self.id = u_id
        self.email = email
        self.status = status
        self.mobile = mobile
        self.phone = phone
        if not self.id:
            Users.cache_invalidate()
            data = [name, email, status, mobile, phone]
            with connection.cursor() as cursor:
                cursor.callproc('create_user', data)
        elif update and self.id:
            Users.cache_invalidate()
            with connection.cursor() as cursor:
                data = [int(u_id), name, email, status, mobile, phone]
                cursor.callproc('update_user', data)
                if isinstance(enroll, list) or isinstance(enroll, tuple):
                    Users.add_membership(user_id=self.id, course_ids=enroll)

    @property
    def memberships(self):
        if self.id:
            return Users.get_memberships(self.id)
        else:
            raise ValueError("User has not 'id'!")

    @property
    def available_courses(self):
        courses = Courses.get_all()
        memberships = self.memberships
        return [courses for courses in courses if courses not in memberships]

    def __str__(self):
        return str(self.name)


class Users:
    """
    Database manager for `users` table
    """
    @staticmethod
    def create_or_update(u_id=None, name=None, email=None,
                         status="Inactive", mobile="", phone="",
                         update=False, memberships=None):

        return User(u_id=u_id, name=name, email=email,
                    status=status, mobile=mobile, phone=phone,
                    update=update, enroll=memberships)

    @staticmethod
    @memoize(timeout=60 * 60)
    def get_all():
        with connection.cursor() as cursor:
            cursor.callproc('get_all_users', [])
            rows = cursor.fetchall()
            return reversed([User(u_id=int(u[0]), name=u[1],
                                  email=u[2], status=u[3],
                                  mobile=u[4], phone=u[5]) for u in rows])

    @staticmethod
    def add_membership(user_id=None, course_ids=None):
        with connection.cursor() as cursor:
            cursor.callproc('delete_memberships', [user_id])
            if course_ids and len(course_ids) > 0:
                [cursor.callproc('create_memberships', [user_id, course_id])
                 for course_id in list(set(course_ids))]

    @staticmethod
    def get_memberships(user_id=None):
        with connection.cursor() as cursor:
            cursor.callproc('get_memberships', [user_id])
            rows = cursor.fetchall()
            return [Course(u[0], u[1], u[2]) for u in rows]

    @staticmethod
    def delete_by_id(user_id=None):
        Users.cache_invalidate()
        with connection.cursor() as cursor:
            cursor.callproc('delete_user', [user_id])

    @staticmethod
    def get_by_id(user_id=None):
        with connection.cursor() as cursor:
            cursor.callproc('get_user', [int(user_id)])
            row = cursor.fetchall()
            if row:
                u = row[0]
                return User(u_id=int(u[0]), name=u[1],
                            email=u[2], status=u[3], mobile=u[4], phone=u[5])
            else:
                raise ValueError("User with id '{0}',"
                                 " does not exist".format(user_id))

    @staticmethod
    def cache_invalidate():
        delete_memoized(Users.get_all)


class Courses:
    """
    Database manager for `courses` table
    """
    @staticmethod
    @memoize(timeout=60 * 60)
    def get_all():
        with connection.cursor() as cursor:
            cursor.callproc('get_all_courses', [])
            rows = cursor.fetchall()
            return [Course(u[0], u[1], u[2]) for u in rows]

    @staticmethod
    def cache_invalidate():
        delete_memoized(Courses.get_all)
