import sys
import os
import shutil
import subprocess

import utils
from constants import TEMPLATES_PATH

def git_init(project_path):
    """Calls 'git init' in {project_path}"""

    print('Creating git repository...', end='')
    sys.stdout.flush()

    if utils.call(['git', 'init', project_path], 'git.log') == 0:
        shutil.copy(os.path.join(TEMPLATES_PATH, 'gitignore.tpl'), 
            os.path.join(project_path, '.gitignore'))

        print("Created: .gitignore")
    else:
        print("failed! Check 'git.log' for further information.")


def get_git_value(key):
    """Same as running: $ git config --get {key}

    Returns: 
        (str) {key}'s value or an empty string if {key} not found
    """
    try:
        command = "git config --get %s" % key
        
        return str(subprocess.check_output(command.split()).strip(), encoding='utf-8')
    except subprocess.CalledProcessError as e:
        return ''
