#!/usr/bin/env sh

chmod +x utility/wait_for_it.sh
sh -c "utility/wait_for_it.sh seeyau_backend:8000 -- echo \"Backend is ready\""

CREATE_CERTIFICATE="openssl req -batch -newkey rsa:2048 -new -nodes -x509 -days 365 -addext \"subjectAltName = IP.1:192.168.1.105\" -keyout \"${KEYS_FOLDER}\"/privkey.pem -out \"${KEYS_FOLDER}\"/fullchain.pem"

if [ ! -d "${KEYS_FOLDER}" ]
  then
    echo "SSL certificates are not present self-signing new ones" &&
    mkdir -p "${KEYS_FOLDER}" && sh -c "$CREATE_CERTIFICATE"
  else
    if openssl x509 -checkend 86400 -noout -in "${KEYS_FOLDER}"/fullchain.pem
      then echo "Certificate is good for another day!"
      else echo "Certificate has expired. Creating new one..." && sh -c "$CREATE_CERTIFICATE"
    fi
fi

./watch-for-certificate-updates.sh &
sleep 2

# Running entrypoint script from base image
./docker-entrypoint.sh nginx -g "daemon off;"