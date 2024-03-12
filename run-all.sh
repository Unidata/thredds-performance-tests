#!/bin/sh

# start tds, no caching config
cd tds/
docker build --no-cache -t thredds-performance-tests:5.5-SNAPSHOT .
docker compose up -d tds-no-caching-network-host
until docker inspect --format "{{json .State.Health.Status }}" tds-no-caching-network-host\
| grep -m 1 '"healthy"'; do sleep 1 ; done

# get tds version info
mkdir -p ../tests/version/
docker cp tds-no-caching-network-host:/usr/local/tomcat/webapps/thredds/META-INF/MANIFEST.MF ../tests/version/

# run tests for no caching config
cd ../tests/
mkdir -p results/
docker build --no-cache -t performance-tests:latest .
docker run --rm --network="host" -v ./results/:/usr/tests/results/ --user $(id -u):$(id -g) performance-tests -d /usr/tests/configs/no_caching_tests

# stop tds
cd ../tds/
docker compose down

# start tds, caching config
docker compose up -d tds-caching-network-host
until docker inspect --format "{{json .State.Health.Status }}" tds-caching-network-host\
| grep -m 1 '"healthy"'; do sleep 1 ; done

# run tests for caching config
cd ../tests/
docker run --rm --network="host" -v ./results/:/usr/tests/results/ --user $(id -u):$(id -g) performance-tests -d /usr/tests/configs/caching_tests

# stop tds
cd ../tds/
docker compose down
