#!/bin/bash

certbot certonly --webroot -w /var/www/certbot --keep-until-expiring --email "${CERTBOT_EMAIL}" --agree-tos --no-eff-email -d "${DOMAIN_NAME}"

trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;