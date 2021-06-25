#!/usr/bin/env python3
import json
import logging
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from plover import PloverDB

SCRIPT_DIR = f"{os.path.dirname(os.path.abspath(__file__))}"


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        handlers=[logging.StreamHandler()])

    plover = PloverDB()
    with open(f"{SCRIPT_DIR}/../kg_config.json") as config_file:
        kg_config = json.load(config_file)

    # Grab the proper KG2c file from git lfs as needed
    if kg_config["download_kg2c"]:
        remote_kg_file_name = kg_config["remote_kg_file_name"]
        if not remote_kg_file_name:
            logging.error(f"If you want to download the KG2c JSON file from git lfs, you must provide the file name to "
                          f"download in kg_config.json (under 'remote_kg_file_name')")
            return
        else:
            kg_json_path = f"{SCRIPT_DIR}/../{remote_kg_file_name}"
            logging.info(f"Downloading {remote_kg_file_name} from git lfs..")
            subprocess.check_call(["git", "clone", "git@github.com:ncats/translator-lfs-artifacts.git"])
            subprocess.check_call(["git", "lfs", "pull", "--include", remote_kg_file_name])
            subprocess.check_call(["mv", f"translator-lfs-artifacts/{remote_kg_file_name}", kg_json_path])
            if remote_kg_file_name.endswith(".gz"):
                subprocess.check_call(["gunzip", kg_json_path])

    plover.build_indexes()


if __name__ == "__main__":
    main()
