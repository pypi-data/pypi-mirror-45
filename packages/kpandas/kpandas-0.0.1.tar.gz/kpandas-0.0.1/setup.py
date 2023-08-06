# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kpandas']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.13.0,<2.0.0', 'pandas>=0.24.0,<0.25.0', 'toml>=0.9,<0.10']

setup_kwargs = {
    'name': 'kpandas',
    'version': '0.0.1',
    'description': "Kristjan's helpers for pandas",
    'long_description': '# kpandas',
    'author': 'Kristjan Strojan',
    'author_email': 'info@kristjan.strojan.com',
    'url': 'https://github.com/kristjanstrojan/kpandas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
