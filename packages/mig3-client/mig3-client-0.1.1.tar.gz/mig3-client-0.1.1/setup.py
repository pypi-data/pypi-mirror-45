# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mig3_client', 'mig3_client.vendors']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'gitpython>=2.1,<3.0',
 'pathlib2>=2.3,<3.0',
 'pytest-json>=0.4.0,<0.5.0',
 'pytest<4',
 'requests>=2.21,<3.0',
 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['mig3 = mig3_client:mig3']}

setup_kwargs = {
    'name': 'mig3-client',
    'version': '0.1.1',
    'description': 'Send test result to Mig3 service',
    'long_description': None,
    'author': 'Matthew de Verteuil',
    'author_email': 'onceuponajooks@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
