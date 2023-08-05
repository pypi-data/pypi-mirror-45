# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cartoasync']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'geolibs-cartoasync',
    'version': '0.0.4',
    'description': 'GeoLibs CARTOasync',
    'long_description': '# GeoLibs-CARTOasync\nAsynchronous Python client for CARTO.\n\n## Features\n\n- [x] SQL API\n- [ ] Batch API\n- [ ] COPY queries\n- [ ] Import API\n- [ ] Read and write Panda\'s DataFrames\n- [ ] Maps API?\n- [ ] Tests\n\n\n## Installation\n\n```bash\npip install cartoasync\n```\n\n## Usage\n\n### SQL API example\n\n```python\nfrom cartoasync import Auth, SQLClient\n\nauth = Auth(username=\'username\', api_key=\'api_key\')\nsql_client = SQLClient(auth)\nresult = await sql_client.send(\'SELECT 1 AS one;\')\n\nprint(result)\n>>> {\n>>>   "rows": [\n>>>     {\n>>>       "one": 1\n>>>     }\n>>>   ],\n>>>   "time": 0.002,\n>>>   "fields": {\n>>>     "one": {\n>>>       "type": "number"\n>>>     }\n>>>   },\n>>>   "total_rows": 1\n>>> }\n```\n\n#### SQL API example, step by step\n\n##### 1. Instantiate an `Auth` object:\n\n###### 1.1. CARTO cloud:\n\n```python\nauth = Auth(username=\'username\', api_key=\'api_key\')\n```\n\n###### 1.2. CARTO OnPremises or cloud organization with an implict user:\n\n```python\nauth = Auth(base_url=\'https://myapp.com/user/username/\', api_key=\'api_key\')\n```\n\n###### 1.3. CARTO OnPremises or cloud organization without an implicit user:\n\n```python\nauth = Auth(base_url=\'https://myapp.com/\', username=\'username\', api_key=\'api_key\')\n```\n\n###### 1.4. SSL:\n\nThe `Auth` constructor has and `ssl` attribute. You can use it for handle to the library a [Python\'s SSL context](https://docs.python.org/3/library/ssl.html#ssl-contexts), or set it to `False` for relaxing certification checks. More info on [AIOHTTP doc](https://docs.aiohttp.org/en/stable/client_advanced.html#ssl-control-for-tcp-sockets).\n\n##### 2. Instantiate the SQLClient and send queries:\n\n###### 2.1. SQLClient\'s own AIOHTTP session:\n\n```python\nsql_client = SQLClient(auth)\nresult = await sql_client.send(\'SELECT 1 AS one;\')\n```\n\n###### 2.2. External AIOHTTP session you need to care until the end of its days:\n\n```python\nimport aiohttp\n\nsql_client = SQLClient(auth)\nresult = await sql_client.send(\'SELECT 1 AS one;\', aiohttp.ClientSession())\n```\n',
    'author': 'Geographica',
    'author_email': 'hello@geographica.com',
    'url': 'https://github.com/GeographicaGS/GeoLibs-CARTOasync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
