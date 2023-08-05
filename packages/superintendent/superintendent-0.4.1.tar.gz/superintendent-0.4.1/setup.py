# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['superintendent',
 'superintendent.controls',
 'superintendent.distributed',
 'superintendent.multioutput']

package_data = \
{'': ['*']}

install_requires = \
['bs4[examples]>=0.0.1,<0.0.2',
 'cachetools>=3.1,<4.0',
 'flask>=1.0,<2.0',
 'html5lib[examples]>=1.0,<2.0',
 'hypothesis[tests]>=4.17,<5.0',
 'ipyevents>=0.4.1,<0.5.0',
 'ipywidgets>=7.4,<8.0',
 'jupyter[tests]>=1.0,<2.0',
 'jupyter_sphinx[documentation]>=0.1.4,<0.2.0',
 'm2r[documentation]>=0.2.1,<0.3.0',
 'matplotlib>=3.0,<4.0',
 'nbconvert[tests]>=5.4,<6.0',
 'nbsphinx[documentation]>=0.4.2,<0.5.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'psycopg2-binary>=2.8,<3.0',
 'pytest-helpers-namespace[tests]>=2019.1,<2020.0',
 'pytest-mock[tests]>=1.10,<2.0',
 'pytest[tests]>=4.4,<5.0',
 'requests[examples]>=2.21,<3.0',
 'schedule>=0.6.0,<0.7.0',
 'scikit-learn>=0.20.3,<0.21.0',
 'scipy>=1.2,<2.0',
 'sphinx[documentation]>=2.0,<3.0',
 'sphinx_rtd_theme[documentation]>=0.4.3,<0.5.0',
 'sqlalchemy>=1.3,<2.0',
 'wordcloud[examples]>=1.5,<2.0']

setup_kwargs = {
    'name': 'superintendent',
    'version': '0.4.1',
    'description': 'Interactive machine learning supervision.',
    'long_description': "# Superintendent\n\n[![Build Status](https://travis-ci.org/janfreyberg/superintendent.svg?branch=master)](https://travis-ci.org/janfreyberg/superintendent)\n[![PyPI version](https://badge.fury.io/py/superintendent.svg)](https://badge.fury.io/py/superintendent)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/janfreyberg/superintendent/master)\n[![Coverage Status](https://coveralls.io/repos/github/janfreyberg/superintendent/badge.svg)](https://coveralls.io/github/janfreyberg/superintendent)\n![Python versions](https://img.shields.io/badge/python-3.5%2B-blue.svg)\n\n\n---\n\n![](logo.png)\n\n**`superintendent`** provides an `ipywidget`-based interactive labelling tool for your data. It allows you to flexibly label all kinds of data. It also allows you to combine your data-labelling task with a statistical or machine learning model to enable quick and practical active learning.\n\n## Getting started\n\nTake a look at the documentation: http://www.janfreyberg.com/superintendent/\n\nIt has some explanations of how the library works, and it also has many examples.\n\nIf you'd like to try the library without installing it, check out the [repository on binder](https://mybinder.org/v2/gh/janfreyberg/superintendent/master?filepath=examples.ipynb).\n\n## Installation\n\n```\npip install superintendent\n```\n\nIf you want to also use the keyboard shortcuts for labelling faster, you will\nalso have to enable the ipyevents jupyter extension:\n\n```\njupyter nbextension enable --py --sys-prefix ipyevents\n```\n\nIf you also want to run the examples, you need three additional packages: `requests`, `bs4` and `wordcloud`. You can install them via pip by running:\n\n```\npip install superintendent[examples]\n```\n\nIf you want to contribute to `superintendent`, you will need to install the test dependencies as well. You can do so with `pip install superintendent[tests,examples]`\n",
    'author': 'Jan Freyberg',
    'author_email': 'jan.freyberg@gmail.com',
    'url': 'https://www.janfreyberg.com/superintendent',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
