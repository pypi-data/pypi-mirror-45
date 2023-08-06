# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pynfce', 'pynfce.nfce', 'pynfce.states']

package_data = \
{'': ['*']}

install_requires = \
['requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'pynfce',
    'version': '0.3.1',
    'description': '',
    'long_description': None,
    'author': 'Matheus Cardoso',
    'author_email': 'matheus.mcas@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
