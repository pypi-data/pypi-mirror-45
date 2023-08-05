# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiub_notes_dl']

package_data = \
{'': ['*']}

install_requires = \
['BeautifulSoup4>=4.7,<5.0', 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['aiubnotesdl = aiub_notes_dl:cli']}

setup_kwargs = {
    'name': 'aiub-notes-dl',
    'version': '1.0.0.post1',
    'description': 'Download notes from AIUB portal',
    'long_description': None,
    'author': 'Fahad Hossain',
    'author_email': 'evilinfinite7@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
