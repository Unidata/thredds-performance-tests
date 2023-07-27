#!/bin/bash
ab -n 100 -e results/test.csv http://localhost:8080/thredds/dodsC/aggregation.ascii
