import os


# Templates directory path
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')

# License templates directory path
LICENSES_PATH = os.path.join(TEMPLATES_PATH, 'licenses')

# PyBuddy config file path
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.pybuddy.ini')