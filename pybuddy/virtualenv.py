import sys
import os

from pybuddy.utils import which, call


def create_virtualenv(path, python_path=None):
    """Setup virtual environment in {path} with {python_path}

    Arguments:
        path:        (str) virtual environment path
        python_path: (str) python executable
    """
    virtualenv = which('virtualenv')

    if not virtualenv:
        raise IOError("Error: No virtualenv executable found.")

    command = [virtualenv]

    # Specify which python executable to  use
    if python_path: 
        command.append('--python')
        command.append(python_path)

    command.append(path)

    print('Creating virtual environment...', end='')
    sys.stdout.flush()

    if call(command, 'virtualenv.log') != 0:
        print("failed! Check 'virtualenv.log' for further information.")
        return

    print("done!")


def create_activate_script(virtualenv_path, project_path):
    path = os.path.join(project_path, 'activate.sh')
    data = "#!/usr/bin/env bash\n. %s/bin/activate" % (virtualenv_path)

    with open(path, 'w') as f:
        f.write(data)

    # Change activate.sh permission
    os.chmod(path, stat.S_IRWXU | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

