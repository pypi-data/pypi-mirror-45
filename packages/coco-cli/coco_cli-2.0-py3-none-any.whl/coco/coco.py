#!/usr/bin/env python3

import json
import os
from pathlib import Path

import click

from . import prompt

CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/database.json'


@click.group()
def cli():
    pass


@cli.command("add", short_help="Add a prompt")
@click.argument("path", required=True, type=click.Path(resolve_path=True))
@click.argument("name", required=True)
def add_prompt(path, name):
    """Add a prompt"""
    add_config_file(path, name)


@cli.command("rm", short_help="Remove a prompt")
@click.argument("name", required=True)
@click.option('--delete-config', is_flag=True)
def remove_prompt(name, delete_config):
    """Remove a prompt

    If the flag --delete-config is present the associated config file
    will also be deleted.
    """

    with open(CONFIG_PATH) as f:
        config = json.load(f)
        path = config[name]
        del config[name]

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

    if delete_config:
        os.remove(path)


@cli.command("ls", short_help="List all prompts")
def list_prompts():
    """List all prompts defined in the config file"""

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    for key, value in config.items():
        print(f"{key} -> {value}")


@cli.command("run", short_help="Run a prompt")
@click.argument("name", required=True)
@click.argument("args", nargs=-1)
def run_prompt(name, args):
    """Run a prompt"""

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    path = config[name]
    if "~" in path:
        absolute_path = Path(path).expanduser()
    else:
        absolute_path = Path(path).resolve()

    prompt.run(absolute_path, *args)


@cli.command("new", short_help="Generate a default config file")
@click.argument("path", required=True, type=click.Path(resolve_path=True))
@click.argument("name", required=True)
def new_entry(path, name):
    """Generate a default config file for a new entry."""

    default_config = {'prompt': "Select command to run:", 'choices': {}}
    with open(path, 'w') as f:
        json.dump(default_config, f)

    add_config_file(path, name)


def add_config_file(path, name):
    entry = {name: path}

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    config.update(entry)

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

