# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['classparse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'classparse',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
