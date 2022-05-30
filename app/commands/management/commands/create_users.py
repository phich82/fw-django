from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from .BaseStyle import BaseStyle

class Command(BaseCommand, BaseStyle):
    """Command for test

    Usage:
        python manage.py runtest {total} {--prefix|-p} {prefix_value} {--admin|-a}
    """

    help = 'Create random users'

    def add_arguments(self, parser):
        # Define an argument (ids)
        parser.add_argument('total', type=int, help='Indicates the number of users to be created.')
        # Optional argument (prefix)
        parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix')
        # Flag Arguments (true | false)
        parser.add_argument('-a', '--admin', action='store_true', help='Create an admin account')

    def handle(self, *args, **options):
        total = options['total']
        prefix = options['prefix']
        admin = options['admin']

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string(10))
            else:
                username = get_random_string(10)

            # if admin:
            #     User.objects.create_superuser(username=username, email='', password='p12345678')
            # else:
            #     User.objects.create_user(username=username, email='', password='p12345678')

            self.stdout.write(self.style.SUCCESS('User%s created successfully => "%s"' % (' (admin)' if admin else '', username)))
            self.info('User%s created successfully => "%s"' % (' (admin)' if admin else '', username))
