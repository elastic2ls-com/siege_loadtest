#!/bin/bash

# function to urlencode username
rawurlencode() {
  local string="${1}"
  local strlen=${#string}
  local encoded=""

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${string:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
  echo "${encoded}"
}

# variables
IFS="|"
URLS=($URL_LIST)
HOSTS=($ETC_HOSTS)

# configure login
if ${USE_LOGIN}; then
    USERNAME_ENCODED=$( rawurlencode "${3}" )
    echo "USERNAME ENCODED = ${USERNAME_ENCODED}"
    LOGIN_URL_ENCODED=$( echo ${2} | sed -e "s/{{USERNAME}}/${USERNAME_ENCODED}/g" | sed -e "s/{{PASSWORD}}/${PASSWORD}/g" )
    echo "login-url = ${DOMAIN}${LOGIN_URL_ENCODED}" >> /etc/siege/siegerc
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
    echo "${DOMAIN}${ENDPOINT}" >> /etc/siege/urls.txt;
done

for ((i=0; i<${#HOSTS[@]}; ++i)); do
    HOST=${HOSTS[$i]}
    echo "${HOST}" >> /etc/hosts;
done

cat /etc/hosts

siege -V
siege "$@" 
