# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['x12_utils']

package_data = \
{'': ['*']}

install_requires = \
['pyx12>=2.3,<3.0']

setup_kwargs = {
    'name': 'x12-utils',
    'version': '0.2.0',
    'description': 'Lightweight utilities for working with x12 EDI',
    'long_description': None,
    'author': 'willingham',
    'author_email': 'thomas@tshows.us',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
