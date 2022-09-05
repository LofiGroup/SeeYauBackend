#!/bin/sh

chmod +x ./wait-for-it.sh

./wait-for-it.sh db:3306 -- echo "Database is ready for commands"

python manage.py migrate
python manage.py collectstatic

gunicorn --bind 0.0.0.0:8000 app.asgi -w 2 -k uvicorn.workers.UvicornWorker