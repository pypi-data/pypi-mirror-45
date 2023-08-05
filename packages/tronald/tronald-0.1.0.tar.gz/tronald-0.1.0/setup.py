# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tronald']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'inquirer>=2.5,<3.0',
 'paramiko>=2.4,<3.0',
 'pylint>=2.3,<3.0']

setup_kwargs = {
    'name': 'tronald',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Filip Weidemann',
    'author_email': 'filip.weidemann@outlook.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
