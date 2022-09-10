FROM nginx:1.23.1

RUN apt-get update
RUN apt-get -y install entr

COPY default.conf.template /etc/nginx/templates/
COPY options-ssl-nginx.conf .
COPY ssl-dhparams.pem .

COPY robots.txt /usr/share/nginx/html/

COPY watch-for-certificate-updates.sh .
RUN chmod +x ./watch-for-certificate-updates.sh
COPY deploy-entrypoint.sh .
COPY dev-entrypoint.sh .
ENTRYPOINT ["sh", "./deploy-entrypoint.sh"]
