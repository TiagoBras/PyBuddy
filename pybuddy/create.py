"""Creates a PyPI project

Arguments:
    name:               (str) name (it can be a path too)
    author:             (str) author
        default = ''
    author_email:       (str) author's email
        default = ''
    version:            (str) initial version
        default = '0.0.1'
    description:        (str) description
        default = ''
    license:            (str) license
        default = 'MIT'
    package_name:       (str) package name
        default = '{name}' in lower case
    module_name:        (str) module's name
        default = '{name}' in lower case
    url:                (str) URL
        default = ''
    entry_point:   (str) application's entry point name
        default = '{name}' in lower case
Notes:
    If the license provided is one of the following:
        (MIT, Apache20, Mozilla20, AGPLv3, GPLv3, LGPLv3, Unlicense)
    it automatically generates a LICENSE file with its complete description.
"""
import os

from pybuddy import utils
from pybuddy.constants import TEMPLATES_PATH, LICENSES_PATH

LICENSES = {
    'agplv3': 'AGPLv3.tpl',
    'apache20': 'Apache20.tpl',
    'gplv3': 'GPLv3.tpl',
    'lgplv3': 'LGPLv3.tpl',
    'mit': 'MIT.tpl',
    'mozilla20': 'Mozilla20.tpl',
    'unlicense': 'Unlicense.tpl'
}

def create_project(name,
                   author='',
                   email='',
                   version='0.0.1',
                   project_description='',
                   license='MIT',
                   package_name=None,
                   module_name=None,
                   url='',
                   entry_point=None):

    # Split path into root directory and project name
    root_dir, project_name = os.path.split(os.path.abspath(name))

    # Template variables
    package_name = package_name or project_name.lower()
    module_name = module_name or project_name.lower()
    entry_point = entry_point or project_name.lower()

    # Directories paths
    project_dir = os.path.join(root_dir, project_name)
    package_dir = os.path.join(project_dir, package_name)
    tests_dir   = os.path.join(project_dir, 'tests')

    # Create the above directories
    for d in [project_dir, package_dir, tests_dir]:
        if not os.path.exists(d):
            os.mkdir(d)
            print("Created: %s" % d)

    # Template values
    template_values = {
        'project_name': project_name,
        'author': author,
        'email': email,
        'version': version,
        'project_description': project_description,
        'license': license,
        'package_name': package_name,
        'module_name': module_name,
        'url': url,
        'entry_point': entry_point
    }

    # Join helpers
    j_templates = lambda x: os.path.join(TEMPLATES_PATH, x)
    j_license   = lambda x: os.path.join(LICENSES_PATH, LICENSES.get(x.lower(), 'Empty.tpl'))
    j_project   = lambda x: os.path.join(project_dir, x)
    j_package   = lambda x: os.path.join(package_dir, "%s.py" % (x))
    j_tests     = lambda x: os.path.join(tests_dir, "test_%s.py" % (x))

    files = {
        j_project('LICENSE.txt'): j_license(license),
        j_project('setup.py'):    j_templates('setup.py.tpl'),
        j_project('README.md'):   j_templates('README.md.tpl'),
        j_project('MANIEST.in'):  j_templates('MANIFEST.in.tpl'),
        j_project('VERSION'):     j_templates('VERSION.tpl'),
        j_project('setup.cfg'):   j_templates('setup.cfg.tpl'),
        j_project('pytest.ini'):  j_templates('pytest.ini.tpl'),
        j_package(module_name):   j_templates('module.py.tpl'),
        j_package('__init__'):    j_templates('__init__.py.tpl'),
        j_tests(module_name):     j_templates('test_module.py.tpl')
    }

    # Create all files
    for new_file, template_file in files.items():
        with open(new_file, 'w') as f:
            f.write(utils.render_template_file(template_file,  **template_values))

        print("Created: %s" % (new_file))

    return project_dir
