# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['modsman_gui']

package_data = \
{'': ['*'], 'modsman_gui': ['images/*']}

install_requires = \
['modsman>=0.5.0,<0.6.0',
 'pygments>=2.3,<3.0',
 'pyqt5>=5.12,<6.0',
 'traitsui>=6.0,<7.0']

entry_points = \
{'console_scripts': ['modsman-gui = modsman_gui:main']}

setup_kwargs = {
    'name': 'modsman-gui',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sargun Vohra',
    'author_email': 'sargun.vohra@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
