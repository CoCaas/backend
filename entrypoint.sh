#!/bin/bash

if [ ! -z $DATABASE_IP ]; then
    sed -i 's/"host":"127.0.0.1"/"host":"'"$DATABASE_IP"'"/g' config.json
    echo "Database IP changed"
fi
if [ ! -z $DATABASE_PORT ]; then
    sed -i 's/"port":"27017"/"port":"'"$DATABASE_PORT"'"/g' config.json
    echo "Database port changed"
fi
if [ ! -z $DATABASE_NAME ]; then
    sed -i 's/"name":"db"/"name":"'"$DATABASE_NAME"'"/g' config.json
    echo "Database name changed"
fi

python /cocass-rest/RestApi.py
