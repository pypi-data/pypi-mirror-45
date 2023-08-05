# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dnstest']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=5.1,<6.0',
 'cerberus>=1.2,<2.0',
 'click>=7.0,<8.0',
 'pydig>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'dnstest',
    'version': '0.1.0a0',
    'description': 'A cli tool for testing DNS records match a provided yaml config file',
    'long_description': '# dnstest\n\nA cli tool for testing DNS records match a provided yaml config file.\n\n[![Build Status](https://travis-ci.org/leonsmith/dnstest.svg?branch=master)](https://travis-ci.org/leonsmith/dnstest)\n[![Python Versions](https://img.shields.io/pypi/pyversions/dnstest.svg)](https://pypi.org/project/dnstest/)\n[![License](https://img.shields.io/pypi/l/dnstest.svg?color=informational)](https://pypi.org/project/dnstest/)\n\n## Versioning\n\ndnstest follows [SemVer](https://semver.org/) (MAJOR.MINOR.PATCH) to track what is in each release.\n\n* Major version number will be bumped when there is an incompatible API change\n* Minor version number will be bumped when there is functionality added in a backwards-compatible manner.\n* Patch version number will be bumped when there is backwards-compatible bug fixes.\n\nAdditional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.\n\n\n## Installation\n\nInstallation the package from pypi with your tool of choice `pip`, `poetry`\nor `pipenv`.\n\n```bash\npip install dnstest\n```\n\n## Usage\n\nTODO:\n\n`dnstest ./example-config.yml`\n\n\n## Documentation\n\nTODO:\n\nhttps://github.com/leonsmith/dnstest/\n\n\n## Support\n*If you’re interested in financially supporting open source, consider donating.*\n\n\n[![XLM Wallet](https://img.shields.io/keybase/xlm/leonsmith.svg)](https://keybase.io/leonsmith)\n[![BTC Wallet](https://img.shields.io/keybase/btc/leonsmith.svg)](https://keybase.io/leonsmith)\n',
    'author': 'Leon Smith',
    'author_email': '_@leonmarksmith.com',
    'url': 'https://github.com/leonsmith/dnstest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
