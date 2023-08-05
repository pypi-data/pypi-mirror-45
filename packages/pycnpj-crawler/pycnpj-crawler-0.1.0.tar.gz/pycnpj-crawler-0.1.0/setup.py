# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pycnpj_crawler', 'pycnpj_crawler.states']

package_data = \
{'': ['*']}

install_requires = \
['pycpfcnpj>=1.5,<2.0', 'requests-html>=0.10.0,<0.11.0', 'unidecode>=1.0,<2.0']

setup_kwargs = {
    'name': 'pycnpj-crawler',
    'version': '0.1.0',
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
