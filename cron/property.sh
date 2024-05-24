#!/usr/bin/env bash

cd ~/outlier-experiments
set -a; source .env; set +a

current_date=$(date +%d%m%Y)

# Start the transaction
psql $DATABASE_URL -c "BEGIN;"

# Run the commands
psql $DATABASE_URL -c "
ALTER TABLE address_lookup.mi_wayne_detroit DROP CONSTRAINT IF EXISTS mi_wayne_detroit_pk;
DROP INDEX IF EXISTS "address_lookup"."mi_wayne_detroit_wkb_geometry_geom_idx";
ALTER TABLE address_lookup.mi_wayne_detroit ALTER COLUMN ogc_fid DROP DEFAULT;
DROP SEQUENCE IF EXISTS address_lookup.mi_wayne_detroit_ogc_fid_seq;
"

# Include the SQL file within the transaction
psql $DATABASE_URL -a  -f ./download/mi_wayne_detroit.sql

# Continue with the commands
psql $DATABASE_URL -c "
ALTER TABLE address_lookup.mi_wayne_detroit RENAME TO mi_wayne_detroit_${current_date};
ALTER TABLE public.mi_wayne_detroit SET SCHEMA address_lookup;
"

# Commit the transaction
psql $DATABASE_URL -c "COMMIT;"

rm ./download/mi_wayne_detroit.sql
rm ./download/mi_wayne_detroit.sql.zip