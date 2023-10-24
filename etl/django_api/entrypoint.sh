#!/bin/sh

echo "Waiting for postgres and elastic search"
while ! (nc -z elastic_search 9200 && nc -z db 5432 && nc -z redis 6379); do
  sleep 0.1
done
exec "$@"