# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['blynclight', 'blynclight.hid', 'blynclight.scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['blync = blynclight.scripts.blync:cli',
                     'fli = blynclight.scripts.fli:cli',
                     'rainbow = blynclight.scripts.rainbow:cli',
                     'throbber = blynclight.scripts.throbber:cli']}

setup_kwargs = {
    'name': 'blynclight',
    'version': '0.4.5',
    'description': 'Python language bindings for Embrava BlyncLight devices.',
    'long_description': None,
    'author': "Erik O'Shaughnessy",
    'author_email': 'erik.oshaughnessy@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
