# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tdameritrade_cli', 'tdameritrade_cli.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'pyexcel-ods>=0.5.6,<0.6.0',
 'tdameritrade-client>=0.3,<0.4']

entry_points = \
{'console_scripts': ['tda-cli = tdameritrade_cli.cli:driver']}

setup_kwargs = {
    'name': 'tdameritrade-cli',
    'version': '0.2.1',
    'description': 'A CLI built on top of the tdameritrade-client API library',
    'long_description': '[![pipeline status](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/badges/master/pipeline.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/commits/master) [![Documentation Status](https://readthedocs.org/projects/tdameritrade-cli/badge/?version=latest)](https://tdameritrade-cli.readthedocs.io/en/latest/?badge=latest) [![coverage report](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/badges/master/coverage.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/commits/master)\n\n\n\n\n# TDAmeritrade CLI\nA CLI that makes requests of TDA using the TDA API via the TDA client. \n\nRead the [docs](https://tdameritrade-cli.readthedocs.io/en/latest/?#).\n\n## Installation:\nFollow the instructions [here](https://tdameritrade-cli.readthedocs.io/en/latest/installation.html) to install the \npackage. \n\n## Usage:\nThe CLI has full help text accessible via `tda-cli --help`. For usage examples, consult the \n[quickstart guide](https://tdameritrade-cli.readthedocs.io/en/latest/quickstart.html).\n',
    'author': 'Joe Castagneri',
    'author_email': 'jcastagneri@gmail.com',
    'url': 'https://gitlab.com/tdameritrade-tools/tdameritrade-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
