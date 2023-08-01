# Thredds performance tests

## Goals:
- locally do performance testing before and after a fix
- automated performance regression tests

## To run the TDS:

Requires docker and docker-compose.

We build a TDS docker image so we are sure to get the latest snapshot. For now, we don't include the netcdf-c library, as that takes 30 minutes to build.

Build the testing docker image:
```
docker build -t thredds-performance-tests:5.5-SNAPSHOT .
```

To start TDS with caching
```
./start-default.sh
```
or without caching
```
./start-no-caching.sh
``````

To stop:
```
./stop.sh
```

## To run the tests:

### With docker
```
cd tests/
docker build -t performance-tests .
docker run performance-tests
```

### With local python environment
Must have python3 and pip installed.
```
cd tests/
pip install -r requirements.txt
./run.py
```

## TODO:
- mount test data
- all tests run with python script
- results written to database
- automated run process on jenkins
- docker build from local war file instead of from nexus
