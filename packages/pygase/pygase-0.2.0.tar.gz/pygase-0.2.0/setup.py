# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pygase']

package_data = \
{'': ['*']}

install_requires = \
['curio>=0.9.0,<0.10.0', 'ifaddr>=0.1.6,<0.2.0', 'u-msgpack-python>=2.5,<3.0']

setup_kwargs = {
    'name': 'pygase',
    'version': '0.2.0',
    'description': 'A lightweight client-server technology and UDP-based network protocol for real-time online gaming.',
    'long_description': "[![Build Status](https://dev.azure.com/pxlbrain/pygase/_apis/build/status/sbischoff-ai.pygase?branchName=master)](https://dev.azure.com/pxlbrain/pygase/_build/latest?definitionId=2&branchName=master)\n![Azure DevOps tests (branch)](https://img.shields.io/azure-devops/tests/pxlbrain/pygase/1/master.svg)\n![Azure DevOps coverage (branch)](https://img.shields.io/azure-devops/coverage/pxlbrain/pygase/1/master.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n![PyPI](https://img.shields.io/pypi/v/pygase.svg)\n# PyGaSe\n**Py**thon**Ga**me**Se**rver\n\nA Python package that contains a versatile lightweight UDP-based client-server API and network protocol for \nreal-time online games.\n\n### Installation:\n```\npip install pygase\n```\n\n## Example\n\n[This example game implements](/chase/) an online game of chase, in which players can move around,\nwhile one of them is the chaser who has to catch another player. A player who has been\ncatched becomes the next chaser and can catch other players after a 5s protection countdown.\n\nFor a complete API documentation look in [here](/docs/api/) (see GitHub if you're on PyPI.org).\n",
    'author': 'Silas Bischoff',
    'author_email': 'silas.bischoff@googlemail.com',
    'url': 'https://github.com/sbischoff-ai/python-game-service',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
