#!/bin/sh
set -e
echo Applying migrations
yoyo apply --database mysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DATABASE --batch
echo Migrations applied
exec "$@"