#!/bin/sh
set -e
if [ $IS_DEV_MODE -eq "0"]; then
    echo Applying migrations in product mode
    yoyo apply --database mysql://$MYSQL_USERNAME:$MYSQL_PASSWORD@$MYSQL_HOST:3306/$MYSQL_DATABASE --batch
else
    echo Applying migrations in dev mode
    yoyo apply --database mysql://$DEV_MYSQL_USERNAME:$DEV_MYSQL_PASSWORD@$DEV_MYSQL_HOST:3306/$DEV_MYSQL_DATABASE --batch
fi
echo Migrations applied
exec "$@"