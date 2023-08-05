import io
import itertools
import sys

import django

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase

from mock import MagicMock

patch = MagicMock().patch


class TestDjangoCreateuser(TestCase):

    n = itertools.count()

    def test_createuser_username_password_email(self):
        n = next(self.n)
        out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
        if django.VERSION >= (2, 1):
            call_command('createuser', 'user%d' % n, password='password%d' % n, email='email%d' % n, verbosity=2, stdout=out)
        else:
            call_command('createuser', 'user%d' % n, '--password', 'password%d' % n, '--email', 'email%d' % n, verbosity=2, stdout=out)
        self.assertEqual(out.getvalue(), 'User user%d created successfully.\n' % n)

        user = get_user_model().objects.get(username='user%d' % n)
        self.assertEqual(user.username, 'user%d' % n)
        self.assertNotEqual(user.password, '')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.email, 'email%d' % n)
        self.assertListEqual(list(user.groups.values_list()), [])

    def test_createuser_no_email(self):
        n = next(self.n)
        try:
            out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
            if django.VERSION >= (2, 1):
                call_command('createuser', 'user%d' % n, password='password%d' % n, verbosity=2, stdout=out)
            else:
                call_command('createuser', 'user%d' % n, '--password', 'password%d' % n, verbosity=2, stdout=out)
            error = out.getvalue()
        except CommandError as e:
            error = e.args[0]
        self.assertIn(error, [
            'Error: the following arguments are required: --email',  # 2.x
            'Error: argument --email is required',  # 1.x
        ])

    def test_createuser_first_name(self):
        n = next(self.n)
        out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
        if django.VERSION >= (2, 1):
            call_command('createuser', 'user%d' % n, password='password%d' % n, email='email%d' % n, first_name='first_name%d' % n, verbosity=2, stdout=out)
        else:
            call_command('createuser', 'user%d' % n, '--password', 'password%d' % n, '--email', 'email%d' % n, '--first_name', 'first_name%d' % n, verbosity=2, stdout=out)
        self.assertEqual(out.getvalue(), 'User user%d created successfully.\n' % n)

        user = get_user_model().objects.get(username='user%d' % n)
        self.assertEqual(user.username, 'user%d' % n)
        self.assertEqual(user.first_name, 'first_name%d' % n)

    def test_createuser_last_name(self):
        n = next(self.n)
        out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
        if django.VERSION >= (2, 1):
            call_command('createuser', 'user%d' % n, password='password%d' % n, email='email%d' % n, last_name='last_name%d' % n, verbosity=2, stdout=out)
        else:
            call_command('createuser', 'user%d' % n, '--password', 'password%d' % n, '--email', 'email%d' % n, '--last_name', 'last_name%d' % n, verbosity=2, stdout=out)
        self.assertEqual(out.getvalue(), 'User user%d created successfully.\n' % n)

        user = get_user_model().objects.get(username='user%d' % n)
        self.assertEqual(user.username, 'user%d' % n)
        self.assertEqual(user.last_name, 'last_name%d' % n)

    def test_createuser_is_staff(self):
        n = next(self.n)
        out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
        if django.VERSION >= (2, 1):
            call_command('createuser', 'user%d' % n, password='password%d' % n, email='email%d' % n, is_staff=True, verbosity=2, stdout=out)
        else:
            call_command('createuser', 'user%d' % n, '--password', 'password%d' % n, '--email', 'email%d' % n, '--is-staff', verbosity=2, stdout=out)
        self.assertEqual(out.getvalue(), 'User user%d created successfully.\n' % n)

        user = get_user_model().objects.get(username='user%d' % n)
        self.assertEqual(user.username, 'user%d' % n)
        self.assertEqual(user.is_staff, True)

    def test_createuser_is_superuser(self):
        n = next(self.n)
        out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
        if django.VERSION >= (2, 1):
            call_command('createuser', 'user%d' % n, password='password%d' % n, email='email%d' % n, is_superuser=True, verbosity=2, stdout=out)
        else:
            call_command('createuser', 'user%d' % n, '--password', 'password%d' % n, '--email', 'email%d' % n, '--is-superuser', verbosity=2, stdout=out)
        self.assertEqual(out.getvalue(), 'User user%d created successfully.\n' % n)

        user = get_user_model().objects.get(username='user%d' % n)
        self.assertEqual(user.username, 'user%d' % n)
        self.assertEqual(user.is_superuser, True)

    @patch('getpass.getpass')
    def test_createuser_no_password(self, mocked_getpass):
        n = next(self.n)
        mocked_getpass.return_value = 'password%d' % n
        out = io.StringIO() if sys.version_info >= (3, 0) else io.BytesIO()
        call_command('createuser', 'user%d' % n, email='email%d' % n, verbosity=2, stdout=out)
        self.assertEqual(out.getvalue(), 'User user%d created successfully.\n' % n)

        user = get_user_model().objects.get(username='user%d' % n)
        self.assertEqual(user.username, 'user%d' % n)
        self.assertNotEqual(user.password, '')
