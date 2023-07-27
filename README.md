# Thredds performance tests

## Goals:
- locally do performance testing before and after a fix
- automated performance regression tests

## To run:

Requires docker and docker-compose.

Build the testing docker image:
```
docker build -t thredds-performance-tests:5.5-SNAPSHOT .
```

To start TDS with caching `./start-default.sh` or without caching `./start-no-caching.sh`.

Currently single tests can be run with e.g. `./test.sh`

To stop: `./stop.sh`

## TODO:
- mount test data
- all tests run with python script
- results written to database
- automated run process on jenkins
- docker build from local war file instead of from nexus
