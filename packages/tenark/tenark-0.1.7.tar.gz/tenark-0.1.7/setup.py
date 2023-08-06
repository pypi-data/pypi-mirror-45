# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tenark',
 'tenark.cataloguer',
 'tenark.common',
 'tenark.models',
 'tenark.provisioner']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tenark',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Esteban Echeverry',
    'author_email': 'eecheverry@nubark.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
