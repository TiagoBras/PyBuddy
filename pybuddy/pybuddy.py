#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import sys
import shutil
import re
import subprocess
import copy
import argparse
import stat

try:
    import configparser
except Exception as e:
    import ConfigParser

def main():
    run(sys.argv[1:])

def run(args):
    configFile = os.path.join(os.path.expanduser('~'), '.pybuddy.ini')
    parser = PyBuddyArgsParser(configFile)
    parsedArgs = parser.parseArguments(args)

    pm = ProjectMaker(
        name=parsedArgs.name, 
        author=parsedArgs.author,
        email=parsedArgs.email,
        version=parsedArgs.version,
        description=parsedArgs.description,
        license=parsedArgs.license,
        package_name=parsedArgs.package_name,
        module_name=parsedArgs.module_name,
        url=parsedArgs.url,
        entry_point=parsedArgs.entry_point
    )

    # Create project
    pm.make()

    # Setup tests
    if not parsedArgs.skip_pytest:
        pm.setupPyTest()

    # Setup a Git repository inside the project
    if not parsedArgs.skip_git_init:
        pm.setupGit()
    
    # Setup a virtual environment inside the project
    if parsedArgs.virtualenv:
        pm.setupVirtualEnvironment()

def displayMessage(s, prefix='', posfix='', ignore=False, output=sys.stdout):
    if not ignore:
        print("%s%s%s" % (prefix, s, posfix), file=output)

def render_string(string, **kwargs):
    """Replaces all {<identifier>} by their respective value"""
    # FIXME: use a simple parser (better performance)

    prog = re.compile(r'{[\w_]+}')

    for k in prog.findall(string):
        string = re.sub(k, kwargs.get(k[1:-1], ''), string)

    return string

def render_file(templateFile, renderedFile, log=True, **kwargs):
    """Renders `templateFile` with kwargs and saves it to `renderedFile`"""
    with open(templateFile) as f_in:
        with open(renderedFile, 'w') as f_out:
            f_out.write(render_string(f_in.read(), **kwargs))

        if log:
            print("Created: %s" % renderedFile)

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

def call(cmd, logFileName, preMsg='', successMsg='', failureMsg='', 
    removeLogOnSuccess=True):
    returnCode = 1

    print(preMsg, end='')
    sys.stdout.flush()

    with open(logFileName, 'w') as log:
        returnCode = subprocess.call(cmd, stdout=log, stderr=log)

    if returnCode == 0:
        print(successMsg)

        if removeLogOnSuccess:
            if os.path.isfile(logFileName):
                os.unlink(logFileName)
    else:
        print(failureMsg)

    return returnCode

def getGetGitValue(key):
    """Same as running: $ git config --get {key}

    Returns: 
        (str) {key}'s value or an empty string if {key} not found
    """
    try:
        command = "git config --get %s" % key
        
        return str(subprocess.check_output(command.split()).strip(), encoding='utf-8')
    except subprocess.CalledProcessError as e:
        return ''

class PyBuddyArgsParser(object):
    """docstring for PyBuddyArgsParser"""
    def __init__(self, configFile=None):
        super(PyBuddyArgsParser, self).__init__()
        
        # First: load default 'name' and 'email' from users' .gitconfig
        self.configValues = {}
        self.configValues.setdefault('author', getGetGitValue('user.name'))
        self.configValues.setdefault('email', getGetGitValue('user.email'))

        self.configValues.setdefault('license', 'MIT')
        self.configValues.setdefault('skip_pytest', False)
        self.configValues.setdefault('skip_git_init', False)
        self.configValues.setdefault('virtualenv', False)

        # Second: load defaults from {configFile}
        if configFile and os.path.isfile(configFile):
            config = ConfigParser.ConfigParser()
            config.read(configFile)

            # Check if 'create' section exists
            if 'create' in config.sections():
                createSection = config['create']

                if 'author' in createSection:
                    self.configValues['author'] = createSection['author']

                if 'email' in createSection:
                    self.configValues['email'] = createSection['email']

                if 'license' in createSection:
                    self.configValues['license'] = createSection['license']

                if 'skip_pytest' in createSection:
                    self.configValues['skip_pytest'] = createSection['skip_pytest']

                if 'skip_git_init' in createSection:
                    self.configValues['skip_git_init'] = createSection.getboolean('skip_git_init')

                if 'virtualenv' in createSection:
                    self.configValues['virtualenv'] = createSection.getboolean('virtualenv')

        self.parser = argparse.ArgumentParser(prog='PROG')
        self.subparsers = self.parser.add_subparsers(description='create, config')

        self._setupCreateSubParser()
        self._setupConfigSubParser()

    def parseArguments(self, args):
        return self.parser.parse_args(args)

    def _setupCreateSubParser(self):
        self.create = self.subparsers.add_parser('create', 
            description="Create a python project")

        self.create.add_argument('name', help="Project's name")
        self.create.add_argument('--author', help="Author's name", 
            default=self.configValues['author'])
        self.create.add_argument('--email', help="Author's email",
            default=self.configValues['email'])
        self.create.add_argument('--description', help="Project's description",
            default='')
        self.create.add_argument('--license', help="Project's license", 
            default=self.configValues['license'])
        self.create.add_argument('--entry-point', help="Application's entry point name",
            default=None)
        self.create.add_argument('--version', help="Project's initial version",
            default='0.0.1')
        self.create.add_argument('--package-name', help="Package name",
            default=None)
        self.create.add_argument('--module-name', help="Module's name",
            default=None)
        self.create.add_argument('--url', help="Project's URL",
            default='')
        self.create.add_argument('--skip-pytest', help="Skips setting up pytest for the project",
            default=self.configValues['skip_pytest'], action='store_true')
        self.create.add_argument('--skip-git-init', help="Skip git repository creation",
            default=self.configValues['skip_git_init'], action='store_true')
        self.create.add_argument('--virtualenv', help="Create a virtual environment",
            default=self.configValues['virtualenv'], action='store_true')
        self.create.add_argument('--virtualenv-python', help="Python path",
            default=None, metavar='PYTHON')

    def _setupConfigSubParser(self):
        """Not implemented"""
        pass 

    def _loadConfigFile(self, configFile, configValues):
        """Not implemented"""
        pass

class PyBuddy(object):
    """docstring for PyBuddy"""
    def __init__(self):
        super(PyBuddy, self).__init__()
        self.arg = arg

class ProjectMaker(object):
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
    def __init__(self, name,  
            author='',
            email='',
            version='0.0.1',
            description='',
            license='MIT',
            package_name=None,
            module_name=None,
            url='',
            entry_point=None):
        super(ProjectMaker, self).__init__()
        # Directory with the templates
        self.TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
    
        # Split path into root directory and project name
        rootDir, projectName = os.path.split(os.path.abspath(name))

        # Template variables
        self.project_name = projectName
        self.author = author
        self.email = email
        self.version = version
        self.project_description = description
        self.license = license
        self.package_name = package_name if package_name else self.project_name.lower()
        self.module_name = module_name if module_name else self.project_name.lower()
        self.url = url 
        self.entry_point = entry_point if entry_point else self.project_name.lower()

        # Template variables in dictionary form
        self.variables = self._getTemplateVariablesDict()

        # Directories paths
        self.projectDir = os.path.join(rootDir, projectName)
        self.packageDir = os.path.join(self.projectDir, self.package_name)
        self.testsDir = os.path.join(self.projectDir, 'tests')

        self.hasProjectBeenCreated = False
    
    def make(self):
        """Creates the project"""

        self._createDirectories()
        self._createProjectFiles()
        self._createProjectModuleFiles()

        self.hasProjectBeenCreated = True

        return self.projectDir

    def setupPyTest(self):
        # Make sure this method can only be called after `make()`
        self._raiseErrorIfProjectNotCreated()

        # Create tests directory
        if not os.path.exists(self.testsDir):
            os.mkdir(self.testsDir)

            print("Created: %s" % self.testsDir)

        testModule = {'test_module_py.tpl': "test_%s.py" % self.module_name}
        
        self._renderFiles(testModule, self.TEMPLATES_DIR, self.testsDir, True)

        projectFiles = {
            'setup_py_testing.tpl': 'setup.py',
            'setup_cfg_testing.tpl': 'setup.cfg',
            'pytest_ini.tpl': 'pytest.ini'
        }
        self._renderFiles(projectFiles, self.TEMPLATES_DIR, self.projectDir, True)

    def setupGit(self):
        # Make sure this method can only be called after `make()`
        self._raiseErrorIfProjectNotCreated()
        
        command = ['git', 'init', self.projectDir]
        preMsg = 'Creating git repository...'
        success = 'done!'
        failute = "failed! Check 'git.log' for further information."

        if call(command, 'git.log', preMsg, success, failute) == 0:
            shutil.copy(os.path.join(self.TEMPLATES_DIR, 'gitignore.tpl'), 
                os.path.join(self.projectDir, '.gitignore'))

            print("Created: .gitignore")

    def setupVirtualEnvironment(self, name='venv', directory=None, python=None):
        """Setup virtual environment with {name} in {directory}

        Arguments:
            name:   (str) virtual environment name
            python: (str) python executable
        """
        # Make sure this method can only be called after `make()`
        self._raiseErrorIfProjectNotCreated()

        directory = directory if directory else self.projectDir

        virtualenv = which('virtualenv')

        if not virtualenv:
            print("Error: No virtualenv executable found.")
            return

        command = [virtualenv]

        # Specify which python executable to  use
        if python: 
            command.append('--python')
            command.append(python)

        # At last, add location and virtual environment name
        command.append(os.path.abspath(os.path.join(directory, name)))

        preMsg = 'Creating virtual environment...'
        success = 'done!'
        failute = "failed! Check 'virtualenv.log' for further information."

        if call(command, 'virtualenv.log', preMsg, success, failute) != 0:
            return
        
        gitignore = os.path.join(self.projectDir, '.gitignore')

        # Add virtual environment to .gitignore if venv is in project
        if os.path.isfile(gitignore) and command[-1].startswith(self.projectDir):
            with open(gitignore, 'a') as f:
                f.write("# Virtual enviroment\n%s/\n" % name)

        # Create activate.sh
        activateFile = os.path.join(self.projectDir, 'activate.sh')

        render_file(os.path.join(self.TEMPLATES_DIR, 'activate_sh.tpl'),
            activateFile,
            venv_path=command[-1])

        # Change activate.sh permission
        os.chmod(activateFile, stat.S_IRWXU | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def _createDirectories(self):
        """Create all the necessary directories

        List of directories: Project, ProjectPackage
        """
        for d in [self.projectDir, self.packageDir]:
            if not os.path.exists(d):
                os.mkdir(d)

                print("Created: %s" % d)

    def _createProjectFiles(self):
        """Create project's default files

        List of files: setup.py, README.md, MANIFEST.in, 
            LICENSE.txt, setup.cfg
        """
        files = {
            'setup_py.tpl': 'setup.py',
            'README_md.tpl': 'README.md',
            'MANIFEST_in.tpl': 'MANIEST.in',
            'VERSION.tpl': 'VERSION',
            'setup_cfg.tpl': 'setup.cfg'
        }
        
        # Render the files declared above
        self._renderFiles(files, self.TEMPLATES_DIR, self.projectDir, True)

        # LICENSE.txt's templates are located in 'licenses' directory
        self._renderFiles({self._licenseTemplateName(): 'LICENSE.txt'}, 
            os.path.join(self.TEMPLATES_DIR, 'licenses'),
            self.projectDir, True
        )

    def _createProjectModuleFiles(self):
        """Create project's default files

        List of files: __init__.py, {module_name}.py
        """
        files = {
            '__init___py.tpl': '__init__.py',
            'module_py.tpl': "%s.py" % self.module_name
        }

        # Render the files declared above
        self._renderFiles(files, self.TEMPLATES_DIR, self.packageDir, True)

    # def _renderFile(self, templateFile, renderedFile, destinyDir, log=True):
    #     """Render a template file"""

    def _renderFiles(self, filesDict, templatesDir, destinyDir, log=True):
        """Renderes files"""
        for k in filesDict.keys():
            render_file(
                os.path.join(templatesDir, k),
                os.path.join(destinyDir, filesDict[k]),
                log,
                **self.variables
            )

    def _licenseTemplateName(self):
        files = {
            'agplv3': 'AGPLv3.tpl',
            'apache20': 'Apache20.tpl',
            'gplv3': 'GPLv3.tpl',
            'lgplv3': 'LGPLv3.tpl',
            'mit': 'MIT.tpl',
            'mozilla20': 'Mozilla20.tpl',
            'unlicense': 'Unlicense.tpl'
        }

        return files.get(self.license.lower(), 'Empty.tpl')

    def _getTemplateVariablesDict(self):
        variables = [
            'project_name', 'author', 'email', 'version', 'project_description',
            'license', 'package_name', 'module_name', 'url',
            'entry_point'
        ]

        d = {}
        for key in variables:
            d.update({key: getattr(self, key)})

        return d

    def _raiseErrorIfProjectNotCreated(self):
        if not self.hasProjectBeenCreated:
            raise RuntimeError("Call ProjectMaker.make() first.")

if __name__ == '__main__':
	main()
