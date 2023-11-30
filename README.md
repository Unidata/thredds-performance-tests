# Thredds performance tests

## Goals:
- locally do performance testing before and after a fix
- automated performance regression tests

## To run:
Requires docker and docker compose.

Currently the test data is in a sub directory in the [thredds-test-data](https://github.com/Unidata/thredds-test-data). To mount the test data create a file `tds/.env` which contains an environment variable with the proper path, e.g.
```
DATA_DIR=/my/path/to/thredds-test-data/local/thredds-test-data/cdmUnitTest/thredds-performance-tests
```

To start TDS (with no caching config), run all tests, and stop TDS:
```
./run-all.sh
```

## To run the TDS:

We build a TDS docker image so we are sure to get the latest snapshot. For now, we don't include the netcdf-c library, as that takes 30 minutes to build.

In the tds directory (`cd tds/`), build the testing docker image:
```
docker build -t thredds-performance-tests:5.5-SNAPSHOT .
```

To build using a local war file instead of the one from nexus, use:
```
cp /path/to/my/thredds.war local-war-file/
docker build -t thredds-performance-tests:5.5-SNAPSHOT --build-arg USE_LOCAL_WAR=true .
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
docker build -t performance-tests:latest .
docker run --rm --network="host" -v ./results/:/usr/tests/results/ performance-tests
```

### With local python environment
Must have python3, pip, and ab (ApacheBench) installed.

For info about the tests parameters that can be set, see
```
./tests/run.py --help
```

To run:
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
Note that the response code is not currently checked in the tests but you can see if requests failed in the logs (`results/run.log`).

