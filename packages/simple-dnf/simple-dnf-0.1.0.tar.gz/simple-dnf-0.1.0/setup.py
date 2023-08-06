# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simple_dnf']

package_data = \
{'': ['*'], 'simple_dnf': ['locales/fr/LC_MESSAGES/*']}

setup_kwargs = {
    'name': 'simple-dnf',
    'version': '0.1.0',
    'description': 'Simple graphical utility for DNF package management',
    'long_description': None,
    'author': 'Arkelis',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
