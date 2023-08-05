# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['autodeploy-tests']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<3.0']

setup_kwargs = {
    'name': 'autodeploy-tests',
    'version': '0.2.12',
    'description': '',
    'long_description': None,
    'author': 'Marco Acierno',
    'author_email': 'marcoaciernoemail@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
