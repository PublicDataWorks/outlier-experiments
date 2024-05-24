#!/usr/bin/env bash
cd ~/outlier-experiments

set -a; source .env; set +a
current_date=$(date +%d%m%Y)

curl "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/RentalStatuses/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson" > ./download/rental.geojson



ogr2ogr -f PGDUMP ./download/rental.sql -lco LAUNDER=NO -lco DROP_TABLE=OFF ./download/rental.geojson


psql $DATABASE_URL -c "
ALTER TABLE address_lookup.residential_rental_registrations DROP CONSTRAINT IF EXISTS Residential_Rental_Registrations_pk;
DROP INDEX IF EXISTS \"address_lookup\".\"Residential_Rental_Registrations_wkb_geometry_geom_idx\";
"

psql $DATABASE_URL -a  -f ./download/rental.sql

psql $DATABASE_URL -c "
ALTER TABLE address_lookup.residential_rental_registrations RENAME TO residential_rental_registrations_${current_date};
ALTER TABLE public.rental SET SCHEMA address_lookup;
ALTER TABLE address_lookup.rental RENAME TO residential_rental_registrations;
"

rm ./download/rental.geojson
rm ./download/rental.sql
