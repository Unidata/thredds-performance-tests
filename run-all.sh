#!/bin/sh

# start tds
cd tds/
docker build -t thredds-performance-tests:5.5-SNAPSHOT .
docker compose up -d tds-no-caching-network-host
until docker inspect --format "{{json .State.Health.Status }}" thredds-performance-tests\
| grep -m 1 '"healthy"'; do sleep 1 ; done

# get tds version info
mkdir -p ../tests/version/
docker cp thredds-performance-tests:/usr/local/tomcat/webapps/thredds/META-INF/MANIFEST.MF ../tests/version/

# run tests
cd ../tests/
mkdir -p results/
docker build -t performance-tests:latest .
docker run --rm --network="host" -v ./results/:/usr/src/app/results/ --user $(id -u):$(id -g) performance-tests

# stop tds
cd ../tds/
docker compose down
