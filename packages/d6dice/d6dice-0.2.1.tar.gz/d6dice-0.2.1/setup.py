# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['d6dice', 'd6dice.test']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'numpy>=1.16,<2.0']

entry_points = \
{'console_scripts': ['dice = d6dice.console:cli']}

setup_kwargs = {
    'name': 'd6dice',
    'version': '0.2.1',
    'description': 'Simulated dice object',
    'long_description': '# d6Dice\n\nd6Dice roller\n\n## Overview\n\nd6Dice is intended for use within d6engine. As a dice and calculation object. \n\n## Install\n\n```bash\npython3 -m venv vpy\nsource vpy/bin/activate\npip install d6dice\n  \n```\n',
    'author': 'Chuck Mo',
    'author_email': 'chuck@d6engine.org',
    'url': 'https://d6engine.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
