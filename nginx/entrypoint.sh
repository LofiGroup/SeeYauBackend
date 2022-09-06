#!/usr/bin/env sh

if [ ! -d "${KEYS_FOLDER}" ]
then mkdir -p "${KEYS_FOLDER}" &&
echo "SSL certificates are not present creating dummy ones" &&
openssl req -batch -newkey rsa:2048 -new -nodes -x509 -days 2 -keyout "${KEYS_FOLDER}"privkey.pem -out "${KEYS_FOLDER}"fullchain.pem
fi

export NGINX_ENTRYPOINT_QUIET_LOGS=0

echo "Running entrypoint script from image"
./docker-entrypoint.sh nginx -g "daemon off;"