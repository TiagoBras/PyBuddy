import os
import sys
import argparse

from pybuddy import config
from pybuddy.git import git_init
from pybuddy.create import create_project
from pybuddy.virtualenv import create_virtualenv

def main():
    args = _parse_args(sys.argv[1:])
    path = create_project(
        name=args.name, 
        author=args.author,
        email=args.email,
        version=args.version,
        project_description=args.description,
        license=args.license,
        package_name=args.package_name,
        module_name=args.module_name,
        url=args.url,
        entry_point=args.entry_point,
        setup_tests=args.tests
    )

    if args.git:
        git_init(path)

    if args.virtualenv:
        create_virtualenv(os.path.join(path, 'venv'))

def _parse_args(args):
    default_values = config.default_config_values()
    create_values = default_values['create']

    parser = argparse.ArgumentParser(description="PyBuddy - Generate a well structured python project")
    # subparsers = parser.add_subparsers(description='create, config')

    # create = subparsers.add_parser('create', 
    #         description="Create a python project")

    parser.add_argument('name', help="Project's name")
    parser.add_argument('--author', help="Author's name", 
        default=create_values['author'])
    parser.add_argument('--email', help="Author's email",
        default=create_values['email'])
    parser.add_argument('--description', help="Project's description",
        default='')
    parser.add_argument('--license', help="Project's license", 
        default=create_values['license'])
    parser.add_argument('--entry-point', help="Application's entry point name",
        default=None)
    parser.add_argument('--tests', help="Add tests to project (py.test framework)", action="store_true", default=False)
    parser.add_argument('--version', help="Project's initial version",
        default=create_values['version'])
    parser.add_argument('--package-name', help="Package name",
        default=None)
    parser.add_argument('--module-name', help="Module's name",
        default=None)
    parser.add_argument('--url', help="Project's URL",
        default='')
    parser.add_argument('--git', help="Create git repository",
        default=create_values['skip_git_init'], action='store_true')
    parser.add_argument('--virtualenv', help="Create a virtual environment",
        default=create_values['virtualenv'], action='store_true')
    parser.add_argument('--virtualenv-python', help="Python path",
        default=None, metavar='PYTHON')


    res = parser.parse_args(args)

    return res

if __name__ == '__main__':
    main()