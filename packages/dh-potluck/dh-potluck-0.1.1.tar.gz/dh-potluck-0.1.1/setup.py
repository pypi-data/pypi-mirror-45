# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dh_potluck']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0']

setup_kwargs = {
    'name': 'dh-potluck',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
