#!/bin/bash

IFS="|"
URLS=($URL_LIST)
HOSTS=($ETC_HOSTS)

#CONFIGURE SIEGE SETTINGS
echo "login-url = ${DOMAIN}${LOGIN_URL}"
echo "login-url = ${DOMAIN}$LOGIN_URL" >> /etc/siege/siegerc
echo "user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" >> /etc/siege/siegerc
echo "username = ${USERNAME}" >> /etc/siege/siegerc
echo "password = ${PASSWORD}" >> /etc/siege/siegerc
echo "follow-location = false" >> /etc/siege/siegerc
echo "internet = true" >> /etc/siege/siegerc
echo "delay = 3" >> /etc/siege/siegerc
echo "show-logfile = false" >> /etc/siege/siegerc

#Add urls to urls.txt for testing.
for ((i=0; i<${#URLS[@]}; ++i)); do
    ENDPOINT=${URLS[$i]}
    echo "${DOMAIN}${ENDPOINT}" >> /etc/siege/urls.txt;
done

#Add host file configs if any.
for ((i=0; i<${#HOSTS[@]}; ++i)); do
    HOST=${HOSTS[$i]}
    echo "${HOST}" >> /etc/hosts;
done

siege -V
siege "$@" 
