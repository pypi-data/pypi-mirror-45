# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lcu_connectorpy']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.6,<6.0', 'watchdog>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['doc = scripts:doc']}

setup_kwargs = {
    'name': 'lcu-connectorpy',
    'version': '1.0.2',
    'description': 'An interface for the LoL client API.',
    'long_description': '# lcu_connectorpy\nA Python implementaion of [this](https://github.com/Pupix/lcu-connector) library.\n\n## Download\n\nVia pip:\n\n```sh\npip install lcu-connectorpy\n```\n\n## Usage\n```py\nfrom lcu_connectorpy import Connector\n\nconn = Connector()\nconn.start()\n\nprint(conn.url, conn.auth, sep=\'\\n\')\n\n>>> https://127.0.0.1:18633\n>>> ("riot", "H9y4kOYVkmjWu_5mVIg1qQ")\n```\n\nSee the [docs](https://zer0897.github.io/lcu_connectorpy/lcu_connectorpy/index.html) for more.\n',
    'author': 'Noah',
    'author_email': 'noah@coronasoftware.net',
    'url': 'https://github.com/Zer0897/lcu_connectorpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
