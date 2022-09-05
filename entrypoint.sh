#!/bin/sh

chmod +x ./wait-for-it.sh

./wait-for-it.sh db:3306 -- echo "Database is ready for commands"

python manage.py migrate

python manage.py runserver 0.0.0.0:8000