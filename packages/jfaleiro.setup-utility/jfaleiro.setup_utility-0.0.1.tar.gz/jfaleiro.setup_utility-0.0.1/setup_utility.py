#
#     setup_utility - Shared helpers for setuptools configuration.
#
#     Copyright (C) 2019 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import glob
import importlib
import logging
import os
import subprocess
import sys

from setuptools import Command
from setuptools.command.test import test as TestCommand
from setuptools.dist import Distribution


def _command(command):
    return subprocess.check_output(command.split()).strip().decode('ascii')


def import_setup_requires(requirements):
    result = []
    for import_, install, f in requirements:
        try:
            lib = importlib.import_module(import_)
        except ModuleNotFoundError as _:
            logging.warning('cannot import %s', import_)
            logging.info('pip installing %s', install)
            logging.info(_command('pip install %s' % install))
            logging.info('re-importing %s', import_)
            lib = importlib.import_module(import_)
        result += [f(lib)]
    return result


setup_requirements = [
    ('setupext.janitor', 'setupext-janitor', lambda x: x.CleanCommand),
    ('setuptools_behave', 'behave', lambda x: x.behave_test),
]

imports = import_setup_requires(setup_requirements)

CleanCommand, BehaveTestCommand = imports


class GradleDistribution(Distribution, object):
    def __init__(self, attrs):
        attrs['name'] = os.getenv('PYGRADLE_PROJECT_NAME')
        attrs['version'] = os.getenv('PYGRADLE_PROJECT_VERSION')


class ToxCommand(TestCommand):
    """
    executes tox for tests
    """
    description = __doc__.strip()
    user_options = [
        ('tox-args=', 'a', "Arguments to pass to tox")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


class LicenseHeaderCommand(Command):
    """
    adds a standard copyright header to all source files
    """
    description = __doc__.strip()
    user_options = [
        ('header-file=', 'f', 'header license file'),
        ('extension=', 'e', 'source file extension'),
    ]

    def initialize_options(self):
        self.header_file = 'HEADER'
        self.extension = '.py'

    def finalize_options(self):
        assert self.header_file is not None, 'header_file is required'
        assert self.extension is not None, 'extension is required'

    def run(self):
        if not os.path.isfile(self.header_file):
            raise Exception("header file '%s' is not a file" %
                            self.header_file)
        for filename in glob.iglob("**/*%s" % self.extension, recursive=True):
            print(filename)
            with open(filename, 'r') as file:
                lines = file.readlines()
            output = []
            phases = ('adding_hashbangs',
                      'removing_previous_comments',
                      'adding_header',
                      'adding_source')
            phase = phases[0]
            for line in lines:
                assert phase in phases, '%s not in %s' % (phase, phases)
                if phase == phases[0]:
                    if line.startswith('#!'):
                        output.append(line)
                    else:
                        phase = phases[1]
                if phase == phases[1]:
                    if line.startswith('#'):
                        pass
                    else:
                        phase = phases[2]
                if phase == phases[2]:
                    with open(self.header_file, 'r') as header_file:
                        header_lines = [l if l.endswith('\n')
                                        else l + '\n' for l in header_file.readlines()]
                        output.extend(['#' + l for l in header_lines])
                    phase = phases[3]
                if phase == phases[3]:
                    output.append(line)
            with open(filename, 'w') as file:
                for line in output:
                    file.write(line)


def _version_from_git(branch, commits, tag):
    if branch == 'master':
        # fatal: No names found, cannot describe anything.
        if tag is None or len(tag.strip()) == 0 or tag.startswith('fatal:'):
            return 'master.dev%s' % commits
        else:
            return tag
    elif branch.startswith('release/'):
        return branch.split('/')[-1] + '.dev%s' % commits
    else:
        return 'no_version.dev%s' % commits


def version_from_git():
    branch_name = _command('git rev-parse --abbrev-ref HEAD')
    logging.info('branch %s', branch_name)
    commits = _command('git rev-list --count %s' % branch_name)
    logging.info('commits %s', commits)
    try:
        tag = _command('git describe --tags --abbrev=0')
    except subprocess.CalledProcessError as _:
        logging.warning('cannot describe tag, will use None')
        tag = None
    logging.info('tag %s', tag)
    return _version_from_git(branch_name, commits, tag)
