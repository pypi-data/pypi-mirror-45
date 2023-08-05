# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['spoffy', 'spoffy.client', 'spoffy.io', 'spoffy.models', 'spoffy.modules']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19,<20', 'cattrs>=0.9,<0.10', 'urlobject>=2,<3']

setup_kwargs = {
    'name': 'spoffy',
    'version': '0.2.0',
    'description': 'Spotify API client with async and sync support',
    'long_description': None,
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
