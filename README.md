# Thredds performance tests

## Goals:
- locally do performance testing before and after a fix
- automated performance regression tests

## To run the TDS:

Requires docker and docker-compose.

We build a TDS docker image so we are sure to get the latest snapshot. For now, we don't include the netcdf-c library, as that takes 30 minutes to build.

In the tds directory (`cd tds/`), build the testing docker image:
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

For info about the tests parameters that can be set, see
```
./tests/run.py --help
```

### With docker
```
cd tests/
docker build -t performance-tests .
docker run --rm performance-tests
```

### With local python environment
Must have python3 and pip installed.
```
cd tests/
pip install -r requirements.txt
./run.py
```

The results of the tests are written to `tests/results/results-timestamp.csv`

## To add a test case

- Either add new catalog to `tds/thredds/catalogs` to be picked up by the `catalogScan`
or else add a file to `tds/data` to be picked up by the `datasetScan`.
- Add a new json file or append to the existing json configs in `tests/configs`, including an "id" for the test and what url will be hit.
Note that the response code is not currently checked in the tests

## TODO:
- mount test data
- automated run process (starting/ stopping tds)
- docker build from local war file instead of from nexus
