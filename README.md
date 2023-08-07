# Thredds performance tests

## Goals:
- locally do performance testing before and after a fix
- automated performance regression tests

## To run:
To start TDS (with no caching config), run all tests, and stop TDS:
```
./run-all.sh
```

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
docker build -t performance-tests:latest .
docker run --rm --network="host" -v ./results/:/usr/src/app/results/ performance-tests
```

### With local python environment
Must have python3, pip, and ab (ApacheBench) installed.
```
cd tests/
pip install -r requirements.txt
./run.py
```

The results of the tests are written to `tests/results/results.csv`

## To add a test case

- Either add new catalog to `tds/thredds/catalogs` to be picked up by the `catalogScan`
or else add a file to `tds/data` to be picked up by the `datasetScan`.
- Add a new json file or append to the existing json configs in `tests/configs`, including an "id" and "name" for the test and what url will be hit.
The test id should be unique. The JSON schema used to validate a test is located in `run.py`.
Note that the response code is not currently checked in the tests but you can see if tests failed in the logs (`results.run.log`).

## TODO:
- mount test data
- option to build TDS docker image from local war file instead of from nexus
- add TDS build info (at least the build date and version) to results
- cli interface to run subset of tests
