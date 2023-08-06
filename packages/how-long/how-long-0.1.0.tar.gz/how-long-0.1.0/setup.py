# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['how_long']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.0,<3.0']

setup_kwargs = {
    'name': 'how-long',
    'version': '0.1.0',
    'description': 'A simple decorator to measure a function excecution time.',
    'long_description': '',
    'author': 'wilfredinni',
    'author_email': 'carlos.w.montecinos@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
