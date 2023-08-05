import getpass
import sys

from django.db import DEFAULT_DB_ALIAS
from django.core import exceptions
from django.core.management import base
from django.contrib.auth import get_user_model, models
from django.core.management.base import CommandError


class NotRunningInTTYException(Exception):
    pass


class Command(base.BaseCommand):
    help = \
        """
        Used to create a user.
        """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.UserModel = get_user_model()

        self.REQUIRED_FIELDS = getattr(self.UserModel, 'REQUIRED_FIELDS', [])
        self.FIELDS = set(self.REQUIRED_FIELDS)

        self.FIRST_NAME_FIELD = getattr(self.UserModel, 'FIRST_NAME_FIELD', 'first_name')
        self.LAST_NAME_FIELD = getattr(self.UserModel, 'LAST_NAME_FIELD', 'last_name')
        self.EMAIL_FIELD = getattr(self.UserModel, 'EMAIL_FIELD', 'email')
        self.USERNAME_FIELD = getattr(self.UserModel, 'USERNAME_FIELD', 'username')
        self.PASSWORD_FIELD = getattr(self.UserModel, 'PASSWORD_FIELD', 'password')

        try:
            if self.UserModel._meta.get_field(self.FIRST_NAME_FIELD):
                self.FIELDS.add(self.FIRST_NAME_FIELD)
        except exceptions.FieldDoesNotExist:
            pass

        try:
            if self.UserModel._meta.get_field(self.LAST_NAME_FIELD):
                self.FIELDS.add(self.LAST_NAME_FIELD)
        except exceptions.FieldDoesNotExist:
            pass

        try:
            if self.UserModel._meta.get_field(self.EMAIL_FIELD):
                self.FIELDS.add(self.EMAIL_FIELD)
        except exceptions.FieldDoesNotExist:
            pass

        try:
            if self.UserModel._meta.get_field(self.PASSWORD_FIELD):
                self.FIELDS.add(self.PASSWORD_FIELD)
        except exceptions.FieldDoesNotExist:
            pass

    def add_arguments(self, parser):
        for field in sorted(self.FIELDS):
            parser.add_argument(
                '--%s' % field, dest=field, default='',
                required=(field in self.REQUIRED_FIELDS),
                help="%s; %s" % (field.capitalize().replace('_', ' '), ('required' if field in self.REQUIRED_FIELDS else 'optional'))
            )
        parser.add_argument(
            '--is-staff', dest='is_staff', action='store_true', default=False,
            help="Staff status; optional, default is False"
        )
        parser.add_argument(
            '--is-superuser', dest='is_superuser', action='store_true', default=False,
            help="Superuser status; optional, default is False"
        )
        parser.add_argument(
            '-g', '--groups', dest='groups', default='',
            help="List of user's groups; optional, comma is a separator"
        )
        parser.add_argument(
            '--database', default=DEFAULT_DB_ALIAS,
            help="Specifies the database to use; optional, default is \"default\"",
        )
        parser.add_argument(
            self.UserModel.USERNAME_FIELD,
            help="Login; required"
        )

    def handle(self, *args, **options):
        groups = []

        for name in options['groups'].split(','):
            if name:
                groups.append(models.Group.objects.get(name=name))

        fields = {
            self.USERNAME_FIELD: options[self.USERNAME_FIELD],
        }

        for field in self.FIELDS:
            fields[field] = options[field]

        if self.PASSWORD_FIELD in self.FIELDS:
            if options[self.PASSWORD_FIELD]:
                fields[self.PASSWORD_FIELD] = options[self.PASSWORD_FIELD]
            else:
                try:
                    while not fields.get(self.PASSWORD_FIELD):
                        password = getpass.getpass()
                        password2 = getpass.getpass('Password (again): ')
                        if password != password2:
                            self.stderr.write("Error: Your passwords didn't match.")
                            # Don't validate passwords that don't match.
                            continue
                        if password.strip() == '':
                            self.stderr.write("Error: Blank passwords aren't allowed.")
                            # Don't validate blank passwords.
                            continue
                        fields[self.PASSWORD_FIELD] = password
                except KeyboardInterrupt:
                    self.stderr.write('\nOperation cancelled.')
                    sys.exit(1)
                except exceptions.ValidationError as e:
                    raise CommandError('; '.join(e.messages))
                except NotRunningInTTYException:
                    self.stdout.write(
                        'User creation skipped due to not running in a TTY. '
                        'You can run `manage.py createuser` in your project '
                        'to create one manually.'
                    )

        # user = self.UserModel.objects.using(options['database']).create_user(**fields)
        user = self.UserModel._default_manager.db_manager(options['database']).create_superuser(**fields)  # pylint: disable=protected-access
        user.is_staff = options['is_staff']
        user.is_superuser = options['is_superuser']
        user.save()

        for g in groups:
            user.groups.add(g)

        verbosity = int(options.get('verbosity', 1))

        if verbosity >= 1:
            self.stdout.write("User %s created successfully." % options[self.USERNAME_FIELD])
