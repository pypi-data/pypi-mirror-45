# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simple_dnf']

package_data = \
{'': ['*'], 'simple_dnf': ['locales/fr/LC_MESSAGES/*']}

entry_points = \
{'console_scripts': ['simple-dnf = simple_dnf:__main__.main']}

setup_kwargs = {
    'name': 'simple-dnf',
    'version': '0.1.1',
    'description': 'Simple graphical utility for DNF package management',
    'long_description': None,
    'author': 'Hyacinthe Pierre Friedrichs',
    'author_email': 'hyakosm@free.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
