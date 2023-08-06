# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrvea',
 'pyrvea.EAs',
 'pyrvea.OtherTools',
 'pyrvea.Population',
 'pyrvea.Problem',
 'pyrvea.Recombination',
 'pyrvea.Selection']

package_data = \
{'': ['*']}

install_requires = \
['diversipy>=0.8.0,<0.9.0',
 'numpy>=1.16,<2.0',
 'optproblems>=1.2,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'plotly>=3.8,<4.0',
 'pyDOE>=0.3.8,<0.4.0',
 'pygmo>=2.10,<3.0',
 'scipy>=1.2,<2.0',
 'tqdm>=4.31,<5.0']

setup_kwargs = {
    'name': 'pyrvea',
    'version': '0.1.0',
    'description': 'The python version reference vector guided evolutionary algorithm.',
    'long_description': None,
    'author': 'Bhupinder Saini',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
