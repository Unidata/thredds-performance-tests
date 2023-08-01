#!/usr/bin/env python3

import glob
import json
import jsonschema

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

def parse_and_validate_configs():
    output = {}

    for config_file in glob.glob("./configs/*"):
        with open(config_file, "r") as file_handle:
            json_contents = json.load(file_handle)
            jsonschema.validate(json_contents, schema=CONFIG_SCHEMA)
            output[config_file] = json_contents

    return output

def run_tests():
    pass
def write_to_csv():
    pass
def parse_cli_args():
    pass

def main():
    test_configs = parse_and_validate_configs()
    print(test_configs)

if __name__ == "__main__":
    main()
