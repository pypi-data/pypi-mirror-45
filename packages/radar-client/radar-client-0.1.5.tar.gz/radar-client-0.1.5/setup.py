# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['radar_client']

package_data = \
{'': ['*']}

install_requires = \
['radar-server>=0.1.4,<0.2.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'radar-client',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Jared Lunde',
    'author_email': 'jared.lunde@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
