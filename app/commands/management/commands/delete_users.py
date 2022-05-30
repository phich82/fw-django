from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from .BaseStyle import BaseStyle

class Command(BaseCommand, BaseStyle):
    help = 'Delete users'

    def add_arguments(self, parser):
        # Arbitrary List of Arguments
        parser.add_argument('user_id', nargs='+', type=int, help='User ID')

    def handle(self, *args, **options):
        users_ids = options['user_id']

        for user_id in users_ids:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                self.success('User "%s (%s)" deleted with success!' % (user.username, user_id))
            except User.DoesNotExist:
                self.error('User with id "%s" does not exist.' % user_id)
