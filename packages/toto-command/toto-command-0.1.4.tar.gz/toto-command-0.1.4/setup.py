# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['toto_command']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['toto-command = toto_command.cli:cli_root']}

setup_kwargs = {
    'name': 'toto-command',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'propaties',
    'author_email': 'sgu02214@nifty.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
