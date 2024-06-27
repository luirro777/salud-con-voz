#!/bin/bash

while ! nc -z "$DDBB_HOST" "$DDBB_PORT"; do
    echo "Esperando al servicio de MySQL..."
    sleep 3
done

exec "$@"