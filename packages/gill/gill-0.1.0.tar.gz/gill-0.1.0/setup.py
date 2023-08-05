# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gill']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.7,<0.30.0']

setup_kwargs = {
    'name': 'gill',
    'version': '0.1.0',
    'description': 'GIL Utilities',
    'long_description': '# gill\n\nUtilities for interacting with the GIL.\n\n```python\nfrom gill import locked_gil\n\n\nwith locked_gil():\n    # No pre-emption from other threads.\n```\n\n# development\n\n```\npoetry install\npoetry build\npoetry publish\n```\n',
    'author': 'Chris Hunt',
    'author_email': 'chrahunt@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
