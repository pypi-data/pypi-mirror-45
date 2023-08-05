# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rs3clans']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6,<0.7']}

setup_kwargs = {
    'name': 'rs3clans',
    'version': '1.1.0',
    'description': "A Python 3 module wrapper for RuneScape 3's API",
    'long_description': None,
    'author': 'johnvictorfs',
    'author_email': 'johnvictorfs@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
