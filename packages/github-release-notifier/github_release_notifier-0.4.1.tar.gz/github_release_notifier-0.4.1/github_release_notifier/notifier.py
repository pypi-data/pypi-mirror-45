# coding: utf-8

import sys
import json
import os
import requests
import logging
import threading
from .webhook import get, get_list
from .parser import parse
from pathlib import Path
from distutils.version import LooseVersion

__DEFAULT_FILE__ = os.getenv('GRN_VERSIONS_FILE', str(Path.home()) + '/.github_release_notifier/versions')


def _call_webhook(webhook: str, entry: str, logger: logging.Logger) -> None:
    logger.info("Hook call : %s / %s" % (webhook, json.dumps(entry)))
    try:
        requests.post(webhook, json=entry)
    except requests.exceptions.RequestException:
        logger.error("Error occurred : %s" % (sys.exc_info()[0]))


def run(file: str = __DEFAULT_FILE__) -> dict:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    updated = {}
    for package in get_list():
        try:
            for entry in parse(package):
                try:
                    condition = LooseVersion(str(entry['version'])) > LooseVersion(str(get_version(package)))
                except TypeError as e:
                    # https://bugs.python.org/issue14894
                    # Always consider the version is new in case of buggy comparision
                    condition = True
                if condition:
                    database = _get_database(file)
                    database[package] = entry['version']
                    _set_database(database, file)
                    updated[package] = entry['version']
                    for webhook in get(package):
                        threading.Thread(target=_call_webhook, args=(webhook, entry, logger,)).start()
        except NameError as e:
            logger.error("Package removed : %s" % package)
            database = _get_database(file)
            del database[package]
            _set_database(database, file)
    return updated


def _get_database(file: str = __DEFAULT_FILE__) -> dict:
    if not Path(file).is_file():
        raise ValueError('Unexpected database file provided')
    return json.loads(open(file, "r").read())


def _set_database(database: dict, filepath: str = __DEFAULT_FILE__) -> None:
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    file = open(filepath, "w+")
    file.write(json.dumps(database))
    file.close()


def get_version(package: str, file: str = __DEFAULT_FILE__) -> str:
    database = _get_database(file)
    return database.get(package, '0.0.0')
