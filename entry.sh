#!/bin/bash

# variables
IFS="|"
URLS=(${URL_LIST})
HOSTS=(${ETC_HOSTS})

# configure login
if ${USE_LOGIN}; then
    echo ${LOGIN_URL}
    echo "login-url = ${DOMAIN}${LOGIN_URL}" >> /etc/siege/siegerc
fi

#CONFIGURE SIEGE SETTINGS
echo "user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" >> /etc/siege/siegerc
echo "follow-location = false" >> /etc/siege/siegerc
echo "internet = true" >> /etc/siege/siegerc
echo "delay = 3" >> /etc/siege/siegerc
cat /etc/siege/siegerc | grep -v '^#'

#Add urls to urls.txt for testing.
for ((i=0; i<${#URLS[@]}; ++i)); do
    ENDPOINT=${URLS[$i]}
    echo "${DOMAIN}${ENDPOINT}" >> /etc/siege/urls.txt
done

for ((i=0; i<${#HOSTS[@]}; ++i)); do
    HOST=${HOSTS[$i]}
    echo "${HOST}" >> /etc/hosts
done

cat /etc/hosts

siege -V
siege "$@" 
