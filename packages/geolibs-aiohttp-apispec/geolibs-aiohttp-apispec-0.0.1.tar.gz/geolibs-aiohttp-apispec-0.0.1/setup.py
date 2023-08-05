# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiohttp_apispec']

package_data = \
{'': ['*'], 'aiohttp_apispec': ['static/*']}

install_requires = \
['aiohttp>=3.5,<4.0',
 'apispec>=1.2.0,<2.0.0',
 'jinja2>=2.10.1,<3.0.0',
 'marshmallow>=2.19,<3.0']

setup_kwargs = {
    'name': 'geolibs-aiohttp-apispec',
    'version': '0.0.1',
    'description': 'GeoLibs aiohttp-apispec',
    'long_description': '# GeoLibs-aiohttp-apispec\n\n### TODO\n- OpenAPI 3\n- Tests\n- Documentation\n  - Installation\n  - Use\n',
    'author': 'Geographica',
    'author_email': 'hello@geographica.com',
    'url': 'https://github.com/GeographicaGS/GeoLibs-aiohttp-apispec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
