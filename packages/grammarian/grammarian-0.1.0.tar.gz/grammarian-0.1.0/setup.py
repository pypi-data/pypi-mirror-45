# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['grammarian']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.7,<5.0',
 'pydictionary>=1.5,<2.0',
 'requests>=2.21,<3.0',
 'urbandictionary>=1.1,<2.0',
 'wikipedia>=1.4,<2.0']

setup_kwargs = {
    'name': 'grammarian',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gabriel Falcão',
    'author_email': 'gabriel@nacaolivre.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
