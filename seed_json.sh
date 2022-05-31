#!/bin/bash

root_dir=app/migrations/seeds/jsons
files=$(ls $root_dir/)

while IFS= read -r file; do
    filepath=$root_dir/$file
    # Only process *.json files
    if [ -f "$filepath" ]; then
        echo -n "Seeding "
        echo $file
        python manage.py loaddata $filepath
    fi
done <<EOF
$files
EOF
