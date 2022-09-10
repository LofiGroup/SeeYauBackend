#!/bin/sh

chmod +x utility/wait_for_it.sh
sh -c "utility/wait_for_it.sh -t 60000 db:3306 -- echo \"Database is ready for commands\""

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8000 app.asgi -w 2 -k uvicorn.workers.UvicornWorker
