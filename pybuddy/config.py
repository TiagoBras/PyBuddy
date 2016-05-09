import os
import sys
import subprocess

from constants import CONFIG_PATH
from git import get_git_value

if sys.version_info < (3,):
    from ConfigParser import ConfigParser 
else:
    from configparser import ConfigParser


def default_config_values():
    default_values  = {
        'create': {
            'author':        get_git_value('user.name'),
            'email':         get_git_value('user.email'),
            'license':       'MIT',
            'version':       '0.0.1',
            'skip_git_init': False,
            'virtualenv':    False
        }
    }

    if not os.path.isfile(CONFIG_PATH):
        return default_values

    config = ConfigParser()
    config.read(CONFIG_PATH)

    # Override the default values with the ones in the config file
    for section in config.sections():
        if section in default_values:
            for key, value in config[section].items():
                if key in default_values[section]:
                    default_values[section][key] = value

    return default_values
