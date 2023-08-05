# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytest_common_subject']

package_data = \
{'': ['*']}

install_requires = \
['lazy-object-proxy>=1.3.1,<2.0.0', 'pytest-lambda>=0.1.0', 'pytest>=3.0,<4.0']

setup_kwargs = {
    'name': 'pytest-common-subject',
    'version': '1.0.0',
    'description': 'pytest framework for testing different aspects of a common method',
    'long_description': '# pytest-common-subject\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'z@perchsecurity.com',
    'url': 'https://github.com/usePF/pytest-common-subject',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
