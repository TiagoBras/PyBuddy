import os
import sys
import argparse

import config

from git import git_init
from create import create_project
from virtualenv import create_virtualenv

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
        entry_point=args.entry_point
    )

    if not args.skip_git_init:
        git_init(path)

    if args.virtualenv:
        create_virtualenv(os.path.join(path, 'venv'))

def _parse_args(args):
    default_values = config.default_config_values()
    create_values = default_values['create']

    parser = argparse.ArgumentParser(prog='PROG')
    subparsers = parser.add_subparsers(description='create, config')

    create = subparsers.add_parser('create', 
            description="Create a python project")

    create.add_argument('name', help="Project's name")
    create.add_argument('--author', help="Author's name", 
        default=create_values['author'])
    create.add_argument('--email', help="Author's email",
        default=create_values['email'])
    create.add_argument('--description', help="Project's description",
        default='')
    create.add_argument('--license', help="Project's license", 
        default=create_values['license'])
    create.add_argument('--entry-point', help="Application's entry point name",
        default=None)
    create.add_argument('--version', help="Project's initial version",
        default=create_values['version'])
    create.add_argument('--package-name', help="Package name",
        default=None)
    create.add_argument('--module-name', help="Module's name",
        default=None)
    create.add_argument('--url', help="Project's URL",
        default='')
    create.add_argument('--skip-git-init', help="Skip git repository creation",
        default=create_values['skip_git_init'], action='store_true')
    create.add_argument('--virtualenv', help="Create a virtual environment",
        default=create_values['virtualenv'], action='store_true')
    create.add_argument('--virtualenv-python', help="Python path",
        default=None, metavar='PYTHON')

    return parser.parse_args(args)

if __name__ == '__main__':
    main()