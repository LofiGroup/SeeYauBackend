#!/bin/bash

if [ ! -f "${KEYS_FOLDER}"/README ]
then rm -r "${KEYS_FOLDER}" && echo "Deleted dummy certificate"
fi

certbot certonly --webroot -w /var/www/certbot --keep-until-expiring --email "${CERTBOT_EMAIL}" --agree-tos --no-eff-email -d "${DOMAIN_NAME}"

#trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;