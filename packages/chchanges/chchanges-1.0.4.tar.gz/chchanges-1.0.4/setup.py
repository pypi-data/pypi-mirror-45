# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chchanges', 'chchanges.demos', 'chchanges.test']

package_data = \
{'': ['*']}

install_requires = \
['imageio>=2.5,<3.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.16,<2.0',
 'pytest>=4.4,<5.0',
 'scipy>=1.2,<2.0']

setup_kwargs = {
    'name': 'chchanges',
    'version': '1.0.4',
    'description': 'Detect statistically meaningful changes in streams of data.',
    'long_description': None,
    'author': 'Jonathan Ward',
    'author_email': 'jon.ward.me@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
