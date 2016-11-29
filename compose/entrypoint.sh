#!/bin/bash

# what set -e means
set -e

USER=jing
APP_UID=$(stat -c "%u" /app)

if [ "$APP_UID" != "0" ]; then
    if [ "$APP_UID" != "$(id -u $USER)" ]; then
        usermod -u "$APP_UID" $USER
    fi
    su $USER -c "$*"
fi

# exec the arguement passed in this bash script
$*
