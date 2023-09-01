#!/bin/sh

cd tds/
docker build -t thredds-performance-tests:5.5-SNAPSHOT .
docker-compose up -d tds-no-caching

until docker inspect --format "{{json .State.Health.Status }}" thredds-performance-tests\
| grep -m 1 "healthy"; do sleep 1 ; done
docker cp thredds-performance-tests:/usr/local/tomcat/webapps/thredds/META-INF/MANIFEST.MF ../tests/version/

cd ../tests/
docker build -t performance-tests:latest .
docker run --rm --network="host" -v ./results/:/usr/src/app/results/ performance-tests

cd ../tds/
docker-compose down
