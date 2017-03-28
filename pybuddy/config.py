import os
import sys
import subprocess

from pybuddy.constants import CONFIG_PATH
from pybuddy.git import get_git_value

if sys.version_info < (3,):
    from ConfigParser import SafeConfigParser
else:
    from configparser import SafeConfigParser

def default_config_values():
    config = SafeConfigParser()
    config.read(CONFIG_PATH)

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

    # Override the default values with the ones in the config file
    for section, options in default_values.items():
        for key in options:
            if section in config.sections(): 
                for key, value in config[section].items():
                    if key in default_values[section]:
                        default_values[section][key] = value

    return default_values
