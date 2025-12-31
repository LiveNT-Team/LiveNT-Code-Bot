#!/bin/sh
set -e
echo Applying migrations
yoyo apply --database mysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:3306/$MYSQL_DATABASE --batch
echo Migrations applied
exec "$@"