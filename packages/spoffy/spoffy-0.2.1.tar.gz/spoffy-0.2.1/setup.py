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
    'version': '0.2.1',
    'description': 'Spotify API client with async and sync support',
    'long_description': '# Spoffy\n\nThe IDE friendly sync and async `Spotify API`_ wrapper for python.\n\nRead the docs: https://spoffy.readthedocs.io\n\n\n# Install\n\n```\npip install spoffy\n```\nPython3.6 and newer are supported\n\n\n\n',
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'url': 'https://github.com/steinitzu/spoffy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
