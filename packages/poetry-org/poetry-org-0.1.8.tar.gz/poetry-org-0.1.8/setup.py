# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['poetry_org']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['poetry-org = poetry_org:main']}

setup_kwargs = {
    'name': 'poetry-org',
    'version': '0.1.8',
    'description': 'Re-organize a single-file app into a poetry directory for building.',
    'long_description': '# poetry-org\nReorganizes files to the same structure as provided with `poetry new` without \ncreating new files. \n\nThis script is useful when using `poetry` to manage a project that was not \ncreated with `poetry new` but was initialized with `poetry init`; the script \nallows conversion from a simple file structure (e.g., `proj_dir/app_name.py`) \ninto a more standard one (e.g., `proj_dir/app_name/app_name.py`) for building \nwith `poetry build`. \n\nThe script moves the app files from the root project directory into a sub-directory \nnamed after the app (as specified in the `pyproject.toml` file), leaving the \nmeta files (e.g., `README.md`, `LICENSE`, `pyproject.toml`) in the root \ndirectory.\n\n# Installation\n\nInstall with `pip` using\n```bash\npip install poetry-org\n```\n\n# Usage\n\nRun in the root directory of the poetry project (where `pyproject.toml` is located). \n```bash\npoetry-org\n```',
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
