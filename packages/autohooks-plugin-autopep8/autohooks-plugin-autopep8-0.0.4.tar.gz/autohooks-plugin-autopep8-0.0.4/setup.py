# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['autohooks', 'autohooks.plugins.autopep8']

package_data = \
{'': ['*']}

install_requires = \
['autohooks>=1.1', 'autopep8']

setup_kwargs = {
    'name': 'autohooks-plugin-autopep8',
    'version': '0.0.4',
    'description': 'Autohooks plugin for code formatting via autopep8',
    'long_description': '# autohooks-plugin-autopep8 [![Build Status](https://travis-ci.com/LeoIV/autohooks-plugin-autopep8.svg?branch=master)](https://travis-ci.com/LeoIV/autohooks-plugin-autopep8)\n\nAn [autohooks](https://github.com/greenbone/autohooks) plugin for python code\nformatting via [autopep8](https://github.com/hhatto/autopep8).\n\n## Installation\n\n### Install using pip\n\nYou can install the latest stable release of autohooks-plugin-autopep8 from the\nPython Package Index using [pip](https://pip.pypa.io/):\n\n    pip install autohooks-plugin-autopep8\n\nNote the `pip` refers to the Python 3 package manager. In a environment where\nPython 2 is also available the correct command may be `pip3`.\n\n### Install using pipenv\n\nIt is highly encouraged to use [pipenv](https://github.com/pypa/pipenv) for\nmaintaining your project\'s dependencies. Normally autohooks-plugin-autopep8 is\ninstalled as a development dependency.\n\n    pipenv install --dev autohooks-plugin-autopep8\n\n## Usage\n\nTo activate the autopep8 autohooks plugin please add the following setting to your\n`pyproject.toml` file.\n\n````toml\n[tool.autohooks]\npre-commit = ["autohooks.plugins.autopep8"]\n````\n### Customizing the `autopep8` behavior\n\nTo pass options to `autopep8`, you have to add an additional \n````toml\n[tool.autohooks.plugins.autopep8]\noption = value\n````\n\nblock to your `pyproject.toml` file. Possible options are explained in the following.\n#### Included files\nBy default, autohooks plugin autopep8 checks all files with a *.py* ending. If only\nfiles in a sub-directory or files with different endings should be formatted,\njust add the following setting:\n\n```toml\ninclude = [\'foo/*.py\', \'*.foo\']\n````\n\n#### Experimental `autopep8` features\nExperimental features can be enabled by adding the following setting:\n```toml\nexperimental-features = true\n```\nThe are disabled by default.\n#### Ignored errors\nYou can specificy which errors should be ignored as follows:\n````toml\nignore_errors = [\'E101\', ...]\n````\nwhere the errors should match to the [list of errors fixed by `autopep8`](https://github.com/hhatto/autopep8).\n\nThe default is `[\'E226\', \'E24\', \'W50\', \'W690\']`.\n\n#### Maximum line length\nThe maximum allowed line length can be set with\n````toml\nmax_line_length = 79\n````\n\nThe default is 79.\n\n\n\n\n## Contributing\n\nYour contributions are highly appreciated. Please\n[create a pull request](https://github.com/LeoIV/autohooks-plugin-autopep8/pulls)\non GitHub. Bigger changes need to be discussed with the development team via the\n[issues section at GitHub](https://github.com/LeoIV/autohooks-plugin-autopep8/issues)\nfirst.\n\n## License\n\nLicensed under the [GNU General Public License v3.0 or later](LICENSE).\n',
    'author': 'Leonard Papenmeier',
    'author_email': 'leonard.papenmeier@posteo.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
