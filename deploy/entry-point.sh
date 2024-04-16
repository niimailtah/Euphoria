#!/bin/bash

set -e

echo "Change variable $API_URL in /etc/nginx/conf.d/default.conf"
sed -i "s@\$\$API_URL@$API_URL@" /etc/nginx/conf.d/default.conf

/usr/sbin/nginx -g 'daemon off;'
