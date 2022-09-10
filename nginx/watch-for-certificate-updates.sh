#!/usr/bin/env sh

CERTS_JUST_DELETED=false
RELOAD_NGINX_COMMAND="/etc/init.d/nginx reload && echo \"nginx successfully reloaded\""

while sleep 2
  do if [ -d "${KEYS_FOLDER}" ]
  then
    if [ $CERTS_JUST_DELETED = true ]
      then echo "Certificates are just added, reloading nginx" && sh -c "${RELOAD_NGINX_COMMAND}" && CERTS_JUST_DELETED=false
    fi
    echo "Watching the certificates" && find "${KEYS_FOLDER}" | entr -p sh -c "echo \"Certificates updated. Reloading nginx...\" && ${RELOAD_NGINX_COMMAND}"
  echo "The directory with certificates is deleted" && CERTS_JUST_DELETED=true
  else echo "No certificates are present, waiting..." && CERTS_JUST_DELETED=true
  fi
done
