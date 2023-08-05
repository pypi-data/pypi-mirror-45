# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['peakipy']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<4.0',
 'bokeh>=1.0.4,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'lmfit>=0.9.12,<0.10.0',
 'matplotlib>=3.0,<4.0',
 'nmrglue>=0.6.0,<0.7.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.0,<0.25.0',
 'scikit-image>=0.14.2,<0.15.0',
 'scipy>=1.2,<2.0']

setup_kwargs = {
    'name': 'peakipy',
    'version': '0.1.0',
    'description': 'Deconvolute overlapping NMR peaks',
    'long_description': None,
    'author': 'Jacob Brady',
    'author_email': 'jacob.brady0449@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
