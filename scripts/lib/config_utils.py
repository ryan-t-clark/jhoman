"""
Utilities to handle parsing and inheritance YAML config files

pip dependencies:
pyyaml
"""

__author__ = "Ryan Clark"

import os
import sys
import yaml
import getpass
import argparse
import datetime as dt
from pathlib import Path
from copy import deepcopy


def load_yaml_file(config_path: str) -> tuple[dict, list[str]]:
    config_path: Path = Path(config_path)

    if not config_path.exists():
        raise RuntimeError(f"Config file does not exist: {config_path}")

    try:
        with open(config_path, 'r') as file:
            config_dict: dict = yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(f"Failed to parse yaml: {e}")

    include_list: list[str] = []
    if 'includes' in config_dict:
        include_list = config_dict['includes']
        include_list = [config_path.parent / path for path in include_list]
        
    return config_dict, include_list


def merge_dicts(primary_config_dict: dict, config_list: list[dict]) -> dict:
    result = {}
    
    for i, config in enumerate(config_list):
        if not isinstance(config, dict):
            print(f"Skipping non-dict item at index {i} in config_list: {type(config)}") # TODO -- get logging in here
            continue
            
        for key, value in config.items():
            if key in result:
                print(f"Key '{key}' being overwritten by config at index {i}") # TODO -- get logging in here
            result[key] = deepcopy(value)
    
    for key, value in primary_config_dict.items():
        if key in result and key != 'includes':
            print(f"Primary config overwriting key '{key}' (previous value: {result[key]})") # TODO -- get logging in here
        result[key] = deepcopy(value)
    
    del result["includes"]

    return result


def load_context(config: dict) -> dict:
    context: dict = {
        "script_name": os.path.basename(sys.argv[0]),
        "start_time": dt.datetime.now(),
        "user": getpass.getuser()
    }

    config['context'] = context

    return config


def load_config(args):
    if not args.config:
        raise RuntimeError(f"No config provided in args")

    primary_config_path: Path = Path(args.config)

    primary_config_dict, include_list = load_yaml_file(primary_config_path)

    config_list: list[dict] = []

    visited_configs: set = set()
    to_visit: list[str] = include_list
    while to_visit:
        for path in to_visit:
            if path in visited_configs:
                to_visit.remove(path)
            else:
                config_dict, include_list = load_yaml_file(path)
                config_list.append(config_dict)
                to_visit.extend(include_list)
                visited_configs.add(path)

    merged_config: dict = merge_dicts(primary_config_dict, config_list)

    config = load_context(merged_config)

    return config


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, type=Path)
    parser.add_argument('-e', '--env', required=False, choices=['DEV', 'TEST', 'PROD'])
    return parser