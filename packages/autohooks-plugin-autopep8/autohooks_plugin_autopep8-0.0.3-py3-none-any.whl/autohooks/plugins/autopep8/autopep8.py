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
from typing import Union, Iterable, List

from autohooks.api import out, ok, error
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match
from autohooks.config import Config

DEFAULT_INCLUDE = ('*.py',)
DEFAULT_EXPERIMENTAL_FEATURES = False
DEFAULT_IGNORE_ERRORS = ['E226', 'E24', 'W50', 'W690']
DEFAULT_MAX_LINE_LENGTH = 79


def check_autopep8_installed():
    try:
        import autopep8  # pylint: disable=unused-import
    except ImportError:
        raise Exception(
            'Could not find autopep8. Please add autopep8 to your python environment'
        )


def get_autopep8_config(config: Config) -> Config:
    return config.get('tool', 'autohooks', 'plugins', 'autopep8')


def get_include_from_config(config: Union[None, Config]) -> Iterable[str]:
    if not config:
        return DEFAULT_INCLUDE

    autopep8_config = get_autopep8_config(config)
    include = autopep8_config.get_value('include', DEFAULT_INCLUDE)

    if isinstance(include, str):
        return [include]

    return include


def get_experimental_features_from_config(config: Union[None, Config]) -> bool:
    if not config:
        return DEFAULT_EXPERIMENTAL_FEATURES
    autopep8_config = get_autopep8_config(config)
    experimental_features = autopep8_config.get_value('experimental-features', DEFAULT_EXPERIMENTAL_FEATURES)
    return experimental_features


def get_ignore_errors_from_config(config: Union[None, Config]) -> List[str]:
    if not config:
        return DEFAULT_IGNORE_ERRORS

    autopep8_config = get_autopep8_config(config)
    ignore_errors = autopep8_config.get_value('ignore_errors', DEFAULT_IGNORE_ERRORS)
    return ignore_errors


def get_default_line_length_from_config(config: Union[None, Config]) -> int:
    if not config:
        return DEFAULT_MAX_LINE_LENGTH

    autopep8_config = get_autopep8_config(config)
    max_line_length = autopep8_config.get_value('max_line_length', DEFAULT_MAX_LINE_LENGTH)
    return max_line_length


def precommit(config=Union[None, Config], **kwargs) -> int:  # pylint: disable=unused-argument
    out('Running autopep8 pre-commit hook')

    check_autopep8_installed()

    include = get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    ignore_errors = get_ignore_errors_from_config(config)

    max_line_length = get_default_line_length_from_config(config)

    experimental = get_experimental_features_from_config(config)

    if len(files) == 0:
        ok('No staged files for autopep8 available')
        return 0

    call_str = ['autopep8', '-i', '-a', '-r', '--ignore', ",".join(ignore_errors), '--max-line-length',
                str(max_line_length)]
    if experimental:
        call_str.append('--experimental')

    with stash_unstaged_changes(files):
        for f in files:
            try:
                subprocess.check_call(
                    call_str + [str(f.absolute_path())])
                ok('Running autopep8 on {}'.format(str(f.path)))
            except subprocess.CalledProcessError as e:
                error('Running autopep8 on {}'.format(str(f.path)))
                raise e

        stage_files_from_status_list(files)

    return 0
