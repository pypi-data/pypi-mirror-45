# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['uvloop>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'linux-touchpad',
    'version': '0.1.0',
    'description': 'Auto-disable laptop touchpad when a mouse is detected.',
    'long_description': None,
    'author': 'Noah',
    'author_email': 'noah@coronasoftware.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
