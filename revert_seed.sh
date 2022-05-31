# !/bin/bash

python manage.py shell < ./app/migrations/revert_seed.py
