#!/usr/bin/env python3

import argparse
import csv
import glob
import json
import logging
import os
import subprocess
import tempfile
from datetime import datetime

import jsonschema
import pandas as pd
import requests

CONFIG_SCHEMA = {
    "type": "object",
    "required": ["name", "id"],
    "properties": {
        "name": {
            "type": "string",
        },
        "id": {
            "type": "string",
            "pattern": "^[a-z_]+([a-z0-9_]+)*$"
        },
        "description": {
            "type": "string",
        },
        "tests": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "id": {
                        "type": "string",
                        "pattern": "^[a-z_]+([a-z0-9_]+)*$"
                    },
                    "description": {
                        "type": "string",
                    },
                    "url": {
                        "type": "string",
                    }
                }
            }
        }
    }
}

BASE_URL = "http://localhost:8080/thredds/"
CONFIG_DIR = os.path.join(".", "configs")
RESULTS_DIR = os.path.join(".", "results")
VERSION_FILE = os.path.join(".", "version", "MANIFEST.MF")
TIME = str(datetime.now().isoformat())
REQUESTS = 1000
TIMELIMIT = 10


def check_ids_are_unique(configs):
    ids = [test["id"] for k, v in configs.items() for test in v["tests"]]
    unique = len(set(ids)) == len(ids)
    if not unique:
        raise ValueError("Expected test ids to be unique, but found:", ids)


def parse_and_validate_configs(args):
    output = {}

    files = glob.glob(os.path.join(args.testdir, "**", "*.json"),
                      recursive=True)
    if not files:
        raise ValueError("No test files found in path: " + args.testdir)

    for config_file in files:
        with open(config_file, "r") as file_handle:
            json_contents = json.load(file_handle)
            jsonschema.validate(json_contents, schema=CONFIG_SCHEMA)
            output[config_file] = json_contents

    check_ids_are_unique(output)
    return output


def get_single_test_config(test_configs, id):
    tests = test_configs.items()
    test = [test for k, v in tests for test in v["tests"] if test["id"] == id]
    if not test:
        raise ValueError("Test case with id: '" + id + "' not found.")
    return {"cli_testcase": {"tests": test}}


def run_tests(test_configs, args):
    df_list = []

    for filename, config in test_configs.items():
        tests = config["tests"]
        for test in tests:
            url = test["url"]
            test_df = run_test(url, test, args)
            df_list.append(test_df)

    return pd.concat(df_list)


def run_test(url, test, args):
    with tempfile.NamedTemporaryFile() as out_file:
        command = [
            "ab",
            "-t",
            str(args.timelimit),
            "-n",
            str(args.requests),
            "-e",
            out_file.name,
            BASE_URL + url
        ]
        out = subprocess.run(
            command,
            capture_output=True,
            text=True)

        logging.info(out.stdout)
        logging.info(out.stderr)
        return make_df(out_file, test)


def make_df(file, test):
    df = pd.read_csv(file)

    df.insert(0, "datetime", TIME)
    df.insert(0, "description", test["description"])
    df.insert(0, "name", test["name"])
    df.insert(0, "id", test["id"])
    return df


def write_to_csv(version_df, df):
    median_time = df.loc[df['Percentage served'] == 50]

    selector = {
        "id": "id",
        "name": "name",
        "description": "description",
        "datetime": "datetime",
        "Time in ms": "median time (ms)"
    }
    data_to_write = median_time.rename(columns=selector)[[*selector.values()]]
    to_write = data_to_write.merge(version_df, on="datetime")

    output_path = os.path.join(RESULTS_DIR, "results.csv")
    to_write.to_csv(
        output_path,
        mode="a",
        header=not os.path.exists(output_path),
        index=False,
        quotechar='"',
        quoting=csv.QUOTE_NONNUMERIC
    )


def parse_cli_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n",
        "--requests",
        nargs="?",
        default=REQUESTS,
        type=int,
        help="Number of requests to execute for each test case."
    )
    parser.add_argument(
        "-t",
        "--timelimit",
        nargs="?",
        default=TIMELIMIT,
        type=int,
        help="Maximum seconds to spend per test case."
    )
    parser.add_argument(
        "-c",
        "--testcase",
        nargs="?",
        type=str,
        help="Specify a specific test case by ID to run"
    )
    parser.add_argument(
        "-d",
        "--testdir",
        nargs="?",
        default=CONFIG_DIR,
        type=str,
        help="Specify a sub directory of tests to run"
    )
    return parser.parse_args()


def check_connection():
    try:
        requests.get(BASE_URL)
    except Exception:
        raise ConnectionError("Cannot connect to TDS at: " + BASE_URL)


def get_tds_version():
    with open(VERSION_FILE, "r") as f:
        contents = f.read().strip().split("\n")
        version_dict = dict(item.split(": ") for item in contents)
        selection = [
            "Implementation-Version",
            "Created-By",
            "Build-Jdk",
            "Built-By",
            "Built-On"
        ]
        selected_dict = {key: [version_dict[key]] for key in selection}
        df = pd.DataFrame(data=selected_dict)
        df.insert(0, "datetime", TIME)

        return df


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(RESULTS_DIR, "run.log"),
        level=logging.INFO,
        filemode="a")

    args = parse_cli_args()
    test_configs = parse_and_validate_configs(args)
    to_test = (test_configs if args.testcase is None
               else get_single_test_config(test_configs, args.testcase))

    check_connection()
    version_df = get_tds_version()
    df = run_tests(to_test, args)
    write_to_csv(version_df, df)


if __name__ == "__main__":
    main()
