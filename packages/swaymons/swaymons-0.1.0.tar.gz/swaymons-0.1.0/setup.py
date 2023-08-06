# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['swaymons']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=1.6,<2.0']

entry_points = \
{'console_scripts': ['swaymons = swaymons']}

setup_kwargs = {
    'name': 'swaymons',
    'version': '0.1.0',
    'description': 'Quickly manage monitons on Sway',
    'long_description': None,
    'author': 'Ranieri Althoff',
    'author_email': '1993083+ranisalt@users.noreply.github.com',
    'url': 'https://gitlab.com/ranisalt/swaymons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
