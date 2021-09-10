#!/usr/bin/env python

import argparse
import logging
from configparser import ConfigParser
from durasftp import Mirrorer


def mirror(mirror_config, callback=None, dry_run=False):
    mirrorer = Mirrorer(**mirror_config)
    mirrorer.mirror_from_remote(callback, dry_run=dry_run)


if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=argparse.FileType("r"),
        dest="configfile",
        default="mirror.ini",
        help="The config file to use",
    )
    args = parser.parse_args()

    # instantiate config parser
    config = ConfigParser(interpolation=None)

    # parse config file
    config.read_file(args.configfile)
    mirror_config = {}
    if not config.has_section("mirror"):
        raise RuntimeError(
            f"ERROR: Config file {args.configfile} missing required mirror section"
        )
    for required_option in ["host", "username", "password", "local_base"]:
        if not config.has_option("mirror", required_option):
            raise RuntimeError(
                f"ERROR: Config file {args.configfile} missing {required_option} in the mirror section"
            )
        else:
            mirror_config[required_option] = config.get("mirror", required_option)

    mirror_config["port"] = 22
    if config.has_option("mirror", "port"):
        mirror_config["port"] = config.getint("mirror", "port")

    dry_run = False
    if config.has_option("mirror", "dry_run"):
        dry_run = config.getboolean("mirror", "dry_run")

    callback = None
    if config.has_option("mirror", "verbosity"):
        verbosity = config.get("mirror", "verbosity").lower().strip()
        if verbosity == "info":
            logging.basicConfig(level=logging.INFO)
            callback = lambda action: print(action)
        elif verbosity == "debug":
            logging.basicConfig(level=logging.DEBUG)
            callback = lambda action: print(action)

    mirror(mirror_config, callback, dry_run)
