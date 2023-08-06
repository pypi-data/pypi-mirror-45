# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['linux-touchpad']

package_data = \
{'': ['*']}

install_requires = \
['uvloop>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'linux-touchpad',
    'version': '0.1.4',
    'description': 'Auto-disable laptop touchpad when a mouse is detected.',
    'long_description': "# Linux Touchpad\n----------------\n\nA simple tool with one job: disable the touchpad on a laptop when a mouse is plugged in.\n\n**Requires**\n\n`Python >= 3.6`\n```\npython -V  # to check\n```\n\n[libinput](https://www.mankier.com/4/libinput) to manage the devices.\n\n\n# Install\n**Recommended**\n\nThe easiest way to get it is through the install script. This will add it to your `~/.local/bin` and configure it to run on startup.\n```\ncurl -sSL https://raw.githubusercontent.com/Zer0897/linux-touchpad/master/install.py | python\n```\n\n*Alternatively*\n\nIt can be done through pip, but you won't get the config setup.\n```\npip install linux-touchpad\n```\n\n## Uninstall\n```\n# Get the file\ncurl -sSL https://raw.githubusercontent.com/Zer0897/linux-touchpad/master/install.py > ~/Downloads/install.py\n# Make it executable\nchmod 777 ~/Downloads/install.py\n# Run the uninstaller\npython ~/Downloads/install.py --uninstall\n```\n\n## Installing Without Startup Behavior\nGet the file as shown above, then run:\n```\npython ~/Downloads/install.py --no-autostart\n```\n\n# Usage\nNote - If startup behavior is enabled (default), it will automatically start when you login.\n\nTo begin:\n```\nlinux-touchpad start&\n```\nOr if installed with pip:\n```\npython -m linux-touchpad start&\n```\nWhile running, this will toggle the touchpad on and off:\n```\nlinux-touchpad toggle\n```\n*Tip: Set this command to a keyboard shortcut for mamimum convenience*\n\nFinally, to stop the process entirely:\n```\nlinux-touchpad kill\n```\n\n\n### Author\nNoah Corona | noah@coronsoftware.net\n",
    'author': 'Noah',
    'author_email': 'noah@coronasoftware.net',
    'url': 'https://github.com/Zer0897/linux-touchpad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
