# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ch', 'ch.debug']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=7.0,<8.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'ch',
    'version': '0.1.1',
    'description': 'utils',
    'long_description': '# ch\n\nVarious utilities to be packaged somewhere else in time.\n',
    'author': 'Chris Hunt',
    'author_email': 'chrahunt@gmail.com',
    'url': 'https://github.com/chrahunt/ch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
