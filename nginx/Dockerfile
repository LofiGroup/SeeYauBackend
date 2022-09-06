FROM nginx:1.23.1

COPY default.conf.template /etc/nginx/templates/
COPY options-ssl-nginx.conf .
COPY ssl-dhparams.pem .

COPY entrypoint.sh .
ENTRYPOINT ["sh", "./entrypoint.sh"]
