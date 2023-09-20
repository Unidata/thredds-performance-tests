#!/bin/sh

cd tds/
docker build -t thredds-performance-tests:5.5-SNAPSHOT .
docker compose up -d tds-no-caching

until docker inspect --format "{{json .State.Health.Status }}" thredds-performance-tests-no-caching\
| grep -m 1 "healthy"; do sleep 1 ; done

cd ../tests/
docker build -t performance-tests:latest .
docker run --rm --network="host" -v ./results/:/usr/src/app/results/ performance-tests

cd ../tds/
docker compose down
