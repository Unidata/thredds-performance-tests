#!/usr/bin/env python3

import glob
import json
import jsonschema
import os
import pandas as pd
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
AB_COMMAND = "ab -t 10 "

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
            out_filename = RESULTS_DIR + test["id"] + ".csv"
            command = AB_COMMAND + "-e " + out_filename + " " + BASE_URL + url
            os.system(command)

            test_df = pd.read_csv(out_filename)
            test_df.insert(0, "time_run", TIME)
            test_df.insert(0, "test_id", test["id"])
            df_list.append(test_df)

    df = pd.concat(df_list)
    print(df.head())
    return df

def write_to_csv(df):
    df.to_csv(RESULTS_DIR + "results-" + TIME + ".csv", index=False)

def parse_cli_args():
    pass

def main():
    test_configs = parse_and_validate_configs()
    print(test_configs)
    df = run_tests(test_configs)
    write_to_csv(df)

if __name__ == "__main__":
    main()
