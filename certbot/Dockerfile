FROM certbot/certbot:v1.29.0

RUN apk update
RUN apk add bash

COPY entrypoint.sh .
ENTRYPOINT ["sh", "./entrypoint.sh"]