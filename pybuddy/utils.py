import re
import sys
import os
import shutil
import subprocess


def render_string(string, **kwargs):
    """Replaces all {<key>} by their respective value"""
    # FIXME: use a simple parser (better performance)

    prog = re.compile(r'{[\w_]+}')

    for k in prog.findall(string):
        string = re.sub(k, kwargs.get(k[1:-1], ''), string)

    return string


def render_template_file(template, **kwargs):
    """Renders a template file

    Arguments:
        template: (str) template file
        **kwargs: (dict) keys/value to be replaced

    Returns: (str) rendered template

    Examples:
        >>> with open('awesome.tpl', 'w') as f:
        >>>     f.write('Hello, I'm {name}! Email me at {email}!')
        >>> render_template_file('awesome.tpl', name='James',
                                 email='james@james.com')
        'Hello, I'm James! Email me at james@james.com'
    """
    with open(template) as f:
        return render_string(f.read(), **kwargs)


def render_file(templateFile, renderedFile, log=True, **kwargs):
    """Renders `templateFile` with kwargs and saves it to `renderedFile`"""
    with open(templateFile) as f_in:
        with open(renderedFile, 'w') as f_out:
            f_out.write(render_string(f_in.read(), **kwargs))

        if log:
            print("Created: %s" % renderedFile)


def call(command, log_file, removeLogOnSuccess=True):
    call_rc = 1

    with open(log_file, 'w') as log:
        call_rc = subprocess.call(command, stdout=log, stderr=log)

    if call_rc == 0 and removeLogOnSuccess:
        if os.path.isfile(log_file):
            os.unlink(log_file)

    return call_rc


def which(filename):
    """Locates a file in the user's PATH

    Returns: (str) file path
    """
    if sys.version_info >= (3,3):
        return shutil.which(filename)
    else:
        for d in os.getenv('PATH').split(os.path.pathsep):
            path = os.path.join(d, filename)
            if os.path.isfile(path):
                return path

    raise IOError("Error: %s not found" % filename)
