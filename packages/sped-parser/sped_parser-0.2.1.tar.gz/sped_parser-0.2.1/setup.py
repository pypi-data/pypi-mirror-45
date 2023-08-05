# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sped_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sped-parser',
    'version': '0.2.1',
    'description': 'manipulate SPED nodes',
    'long_description': None,
    'author': 'Tiago Guimaraes',
    'author_email': 'tilacog@protonmail.com',
    'url': 'https://gitlab.com/tilacog/sped_parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
