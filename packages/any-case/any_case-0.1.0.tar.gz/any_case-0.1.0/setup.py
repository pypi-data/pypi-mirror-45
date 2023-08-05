# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['any_case', 'any_case.contrib', 'any_case.contrib.django']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'any-case',
    'version': '0.1.0',
    'description': 'Snake/Camle case converter with django and rest_framework integration',
    'long_description': None,
    'author': 'asduj',
    'author_email': 'asduj@ya.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
