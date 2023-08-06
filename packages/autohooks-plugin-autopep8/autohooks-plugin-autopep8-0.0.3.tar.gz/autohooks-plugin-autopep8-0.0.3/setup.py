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
    'version': '0.0.3',
    'description': 'Autohooks plugin for code formatting via autopep8',
    'long_description': None,
    'author': 'Leonard Papenmeier',
    'author_email': 'leonard.papenmeier@posteo.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
