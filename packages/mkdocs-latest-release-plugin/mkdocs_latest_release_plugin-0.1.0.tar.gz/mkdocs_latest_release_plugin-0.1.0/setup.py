# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mkdocs_latest_release_plugin']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=2.1.11,<3.0.0',
 'jinja2>=2.10.1,<3.0.0',
 'mkdocs>=1.0.4,<2.0.0',
 'natsort>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'mkdocs-latest-release-plugin',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Garner',
    'author_email': 'andrew@kaizenit.ltd',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
