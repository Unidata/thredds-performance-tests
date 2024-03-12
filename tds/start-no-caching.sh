#!/bin/sh
docker compose up -d tds-no-caching
until docker inspect --format "{{json .State.Health.Status }}" tds-no-caching\
| grep -m 1 '"healthy"'; do sleep 1 ; done

mkdir -p ../tests/version/
docker cp tds-no-caching:/usr/local/tomcat/webapps/thredds/META-INF/MANIFEST.MF ../tests/version/
