# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess

from autohooks.api import out, ok, error
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.py',)


def check_autopep8_installed():
    try:
        import autopep8  # pylint: disable=unused-import
    except ImportError:
        raise Exception(
            'Could not find autopep8. Please add autopep8 to your python environment'
        )


def get_autopep8_config(config):
    return config.get('tool', 'autohooks', 'plugins', 'autopep8')


def get_include_from_config(config):
    if not config:
        return DEFAULT_INCLUDE

    autopep8_config = get_autopep8_config(config)
    include = autopep8_config.get_value('include', DEFAULT_INCLUDE)

    if isinstance(include, str):
        return [include]

    return include


def precommit(config=None, **kwargs):  # pylint: disable=unused-argument
    out('Running autopep8 pre-commit hook')

    check_autopep8_installed()

    include = get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    if len(files) == 0:
        ok('No staged files for autopep8 available')
        return 0

    with stash_unstaged_changes(files):
        for f in files:
            try:
                subprocess.check_call(['autopep8', '-i', '-a', str(f.absolute_path())])
                ok('Running autopep8 on {}'.format(str(f.path)))
            except subprocess.CalledProcessError as e:
                error('Running autopep8 on {}'.format(str(f.path)))
                raise e

        stage_files_from_status_list(files)

    return 0
