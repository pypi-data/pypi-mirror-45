# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['mathlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mathlib',
    'version': '0.1.1',
    'description': 'A pure-python maths library',
    'long_description': '<p align="center">\n<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nA pure python mathematics library\n',
    'author': 'spapanik',
    'author_email': 'spapanik21@gmail.com',
    'url': 'https://github.com/spapanik/mathlib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
