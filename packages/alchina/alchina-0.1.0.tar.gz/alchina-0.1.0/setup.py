# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['alchina']

package_data = \
{'': ['*']}

install_requires = \
['black>=18.3-alpha.0,<19.0',
 'bump2version>=0.5.10,<0.6.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'pytest-cov>=2.6,<3.0',
 'scikit-learn>=0.20.3,<0.21.0']

setup_kwargs = {
    'name': 'alchina',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'matthieu',
    'author_email': 'matthieu.gouel@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
