from django_seed import Seed
from django.contrib.auth.models import User
from app.migrations.echo import echo

from accounts.models import Account

# https://faker.readthedocs.io/en/latest/locales.html
locale = 'en_US', # vi_VN, ja_JP, zh_CN, ko_KR
seeder = Seed.seeder(locale)

########################### SEED HERE ############################

# No specify columns
# seeder.add_entity(Account, 10)

# Specify columns
seeder.add_entity(Account, 10, {
    'user': User.objects.first(),
    'name': lambda x: seeder.faker.user_name()
})

######################## END - SEED HERE #########################

echo(inserted_pks=seeder.execute())
