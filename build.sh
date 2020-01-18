#!/bin/bash

mkdir -p runtime/db
mkdir -p runtime/static
mkdir -p runtime/backend
mkdir -p runtime/frontend
mkdir -p runtime/grafana
mkdir -p runtime/prometheus

cp -r build/grafana/grafana.ini runtime/grafana/grafana.ini
cp -r build/prometheus/prometheus.yml runtime/prometheus/prometheus.yml
cp -r src/backend/* runtime/backend/

docker run --rm \
    -v $(pwd)/src/frontend:/srv/frontend \
    -v $(pwd)/.cache/npm:/root/.npm \
    -v $(pwd)/.cache/yarn:/usr/local/share/.cache/yarn \
    -w /srv/frontend \
    --name frontend-builder \
    -it node:13 sh -c "yarn install && yarn build"

cp -r src/frontend/dist/* runtime/frontend/
