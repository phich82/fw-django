#!/bin/bash

root_dir=app/migrations/seeds
files=$(ls $root_dir/)

while IFS= read -r file; do
    filepath=$root_dir/$file
    # Only process *.py files
    if [ -f "$filepath" ]; then
        echo -n "Seeding "
        echo $file
        python manage.py shell < $filepath
    fi
done <<EOF
$files
EOF
