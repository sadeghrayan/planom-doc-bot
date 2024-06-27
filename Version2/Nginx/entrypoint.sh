#!/bin/sh

# Replace environment variables in the Nginx configuration template
#envsubst '$PROXY_IP' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf
envsubst '$PROXY_IP $KIBANA_PORT $APP_PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Start Nginx
nginx -g 'daemon off;'
