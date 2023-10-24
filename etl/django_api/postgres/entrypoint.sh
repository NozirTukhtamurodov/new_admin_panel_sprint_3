set -e

# Run the PostgreSQL entrypoint script
/usr/local/bin/docker-entrypoint.sh "$@"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE SCHEMA IF NOT EXISTS $POSTGRES_SCHEMA;"
echo "ALTER ROLE $POSTGRES_USER SET search_path = $POSTGRES_SCHEMA, public;" | psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
