#!/bin/bash

if ${IS_DEBUG_VERSION}; then
  echo "It's a debug version, there is no need for certbot. Exiting..."
  exit 0
fi

chmod +x /utility/wait_for_it.sh
bash /utility/wait_for_it.sh "${NGINX_ADDRESS}" -t "${WAIT_FOR_IT_TIME}" -- echo "Nginx is ready"

if [ ! -f "${KEYS_FOLDER}"/README ]
  then rm -r "${KEYS_FOLDER}" && echo "Deleted dummy certificate"
fi

certbot certonly --webroot -w /var/www/certbot --keep-until-expiring --email "${CERTBOT_EMAIL}" --agree-tos --no-eff-email -d "${DOMAIN_NAME}"

trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;