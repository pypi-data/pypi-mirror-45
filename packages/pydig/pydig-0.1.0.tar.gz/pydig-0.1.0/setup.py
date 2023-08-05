# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydig',
    'version': '0.1.0',
    'description': "Python wrapper library for the 'dig' command line tool",
    'long_description': '',
    'author': 'Leon Smith',
    'author_email': '_@leonmarksmith.com',
    'url': 'https://github.com/leonsmith/pydig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
