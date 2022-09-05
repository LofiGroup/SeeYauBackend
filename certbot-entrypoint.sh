#!/bin/sh

certonly --webroot --webroot-path=/usr/share/nginx/html/letsencrypt --email "${CERTBOT_EMAIL}" --agree-tos --no-eff-email -d "${DOMAIN_NAME}"

0 */12 * * * root certbot -q renew --nginx
