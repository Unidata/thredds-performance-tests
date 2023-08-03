#!/usr/bin/env python3

import glob
import io
import json
import jsonschema
import os
import pandas as pd
import subprocess
import time

CONFIG_SCHEMA = {
    "type" : "object",
    "required" : ["name", "id"],
    "properties" : {
        "name" : {
            "type" : "string",
        },
        "id" : {
            "type" : "string",
            "pattern" : "^[a-z_]+([a-z0-9_]+)*$"
        },
        "description" : {
            "type" : "string",
        },
        "tests" : {
            "type" : "array",
            "items" : {
                "type" : "object",
                "required" : ["name", "url"],
                "properties" : {
                    "name" : {
                        "type" : "string",
                    },
                    "id" : {
                        "type" : "string",
                        "pattern" : "^[a-z_]+([a-z0-9_]+)*$"
                    },
                    "description" : {
                        "type" : "string",
                    },
                    "url" : {
                        "type" : "string",
                    }
                }
            }
        }
    }
}

BASE_URL = "http://localhost:8080/thredds/"
CONFIG_DIR = "./configs/"
RESULTS_DIR = "./results/"
TIME = time.strftime("%Y%m%d-%H%M")
REPEAT = 1

def parse_and_validate_configs():
    output = {}

    for config_file in glob.glob(CONFIG_DIR + "*"):
        with open(config_file, "r") as file_handle:
            json_contents = json.load(file_handle)
            jsonschema.validate(json_contents, schema=CONFIG_SCHEMA)
            output[config_file] = json_contents

    return output

def run_tests(test_configs):
    df_list = []

    for filename, config in test_configs.items():
        tests = config["tests"]
        for test in tests:
            url = test["url"]
            out = subprocess.run(["ab", "-n", str(REPEAT), "-e", "/dev/stdout", BASE_URL + url], capture_output=True, text=True)

            test_df = make_df(out.stdout, test["id"])
            df_list.append(test_df)

    df = pd.concat(df_list)
    return df

def make_df(output, test_id):
    start_index = output.index("Percentage served")
    end_index = output.index("..done")
    df = pd.read_csv(io.StringIO(output[start_index:end_index]))

    df.insert(0, "time_run", TIME)
    df.insert(0, "test_id", test_id)
    return df

def write_to_csv(df):
    df.to_csv(RESULTS_DIR + "results-" + TIME + ".csv", index=False)

def parse_cli_args():
    pass

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    test_configs = parse_and_validate_configs()
    df = run_tests(test_configs)
    write_to_csv(df)

if __name__ == "__main__":
    main()
