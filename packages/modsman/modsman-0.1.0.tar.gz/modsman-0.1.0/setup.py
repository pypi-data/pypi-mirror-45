# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['modsman']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'aiohttp>=3.5,<4.0',
 'pathlib>=1.0,<2.0',
 'requests>=2.21,<3.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['modsman = modsman:main']}

setup_kwargs = {
    'name': 'modsman',
    'version': '0.1.0',
    'description': 'A Minecraft mod manager for the command line.',
    'long_description': None,
    'author': 'Sargun Vohra',
    'author_email': 'sargun.vohra@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
