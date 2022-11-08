#!/bin/bash

chmod +x utility/wait_for_it.sh
bash utility/wait_for_it.sh "${DB_HOST}":3306 -t "${WAIT_FOR_IT_TIME}" -- echo "Database is ready for commands"

python manage.py migrate
python manage.py collectstatic --noinput


if (( DEBUG == 1 )); then
  echo "Running porter"
  python run runporter.py &
fi


#gunicorn --bind 0.0.0.0:80 app.asgi -w 2 -k uvicorn.workers.UvicornWorker
daphne -b 0.0.0.0 -p 80 app.asgi:application
