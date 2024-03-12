#!/bin/sh
docker compose up -d tds-caching
until docker inspect --format "{{json .State.Health.Status }}" tds-caching\
| grep -m 1 '"healthy"'; do sleep 1 ; done

mkdir -p ../tests/version/
docker cp tds-caching:/usr/local/tomcat/webapps/thredds/META-INF/MANIFEST.MF ../tests/version/
