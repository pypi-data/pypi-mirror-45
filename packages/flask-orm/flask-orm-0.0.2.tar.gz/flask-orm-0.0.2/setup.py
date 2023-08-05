# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flask_orm']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0',
 'pytest>=4.4,<5.0',
 'sqlalchemy-stubs>=0.1.0,<0.2.0',
 'sqlalchemy>=1.3,<2.0',
 'typing-extensions>=3.7,<4.0']

setup_kwargs = {
    'name': 'flask-orm',
    'version': '0.0.2',
    'description': 'an easy way to use sqlalchemy in your flask app',
    'long_description': None,
    'author': 'kyle roux',
    'author_email': 'jstacoder@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
