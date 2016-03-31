"""Utilities for handling settings."""
import json
import os

# config file path
DEFAULT_SERVER_ADDRESS = "http://private-a6e53-dpcs.apiary-mock.com/"
FILE = os.path.expanduser('~/.dpcs/.dpcsconfig')

DEFAULT_SETTINGS = {'server_address': DEFAULT_SERVER_ADDRESS}


def read_settings():
    try:
        with open(FILE, 'r') as f:
            try:
                settings = json.load(f)
                if 'server_address' not in settings:
                    settings['server_address'] = DEFAULT_SERVER_ADDRESS
            except ValueError:
                settings = DEFAULT_SETTINGS
            return settings
    except IOError:
        return DEFAULT_SETTINGS
