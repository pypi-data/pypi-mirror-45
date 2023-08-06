# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['import_x', 'import_x.loaders']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'import-x',
    'version': '0.1.0',
    'description': 'Import non-python files',
    'long_description': 'import-x\n########\n\nAn ext-tensible loader to import anything like it is a python module.\n\nSupports Python **3.6+**.\n\nUsage\n======\n\nExample json file in your path ``foo.json``:\n\n.. code:: json\n\n    {\n        "why": "not",\n    }\n\n.. code-block:: python\n\n   # Extend the ExtensionLoader and implement \'handle_module\' method\n   # where you will get a module object and the path to that module.\n\n   >>> from import_x import ExtensionLoader\n\n   >>> class JsonLoader(ExtensionLoader):\n        extension = \'.json\'\n\n        auto_enable = False\n\n        @staticmethod\n        def handle_module(module, path):\n            """\n            Load the json file and set as `data` attribute of the module.\n            """\n            json_file = Path(path)\n            content = json_file.read_text()\n            try:\n                data = json.loads(content)\n            except (json.JSONDecodeError, ValueError):\n                data = {}\n            module.data = data\n\n    >>> json_imports = JsonLoader()\n    >>> with json_imports:\n            import foo\n    >>> foo.data\n    >>> {"why": "not"}\n\nIf you want to enable imports automatically without the context_manager then just\ndo ``auto_enable = True`` in your loader.\n',
    'author': 'Mohit Solanki',
    'author_email': 'mohit@deepsource.io',
    'url': 'https://github.com/deepsourcelabs/import-x',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
