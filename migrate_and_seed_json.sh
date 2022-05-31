# !/bin/bash

python manage.py migrate

root_dir=app/migrations/seeds/jsons
files=$(ls $root_dir/)

while IFS= read -r file; do
    filepath=$root_dir/$file
    if [ -f "$filepath" ]; then
        echo -n "Seeding "
        echo $file
        python manage.py loaddata $filepath
    fi
done <<EOF
$files
EOF
