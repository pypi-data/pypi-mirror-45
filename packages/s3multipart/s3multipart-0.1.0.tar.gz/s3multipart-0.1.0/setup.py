# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['s3multipart']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['s3multipart = s3multipart.cli:main']}

setup_kwargs = {
    'name': 's3multipart',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'davido-bs',
    'author_email': 'david.oliver@strategic-i.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
