#!/bin/sh
docker-compose up -d tds-default
until docker inspect --format "{{json .State.Health.Status }}" thredds-performance-tests\
| grep -m 1 "healthy"; do sleep 1 ; done
docker cp thredds-performance-tests:/usr/local/tomcat/webapps/thredds/META-INF/MANIFEST.MF ../tests/version/
