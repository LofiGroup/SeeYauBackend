FROM nginx:1.23.1

COPY ./default.conf /etc/nginx/conf.d/default.conf
RUN apt-get update; sudo apt-get install certbot; apt-get install python3-certbot-nginx

CMD sudo certbot --nginx -d lofigorup-plum.fun www.lofigorup-plum.fun
CMD 0 12 * * * /usr/bin/certbot renew --quiet
