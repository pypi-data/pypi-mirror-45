# poetry-org
Reorganizes files to the same structure as provided with `poetry new` without 
creating new files. 

This script is useful when using `poetry` to manage a project that was not 
created with `poetry new` but was initialized with `poetry init`; the script 
allows conversion from a simple file structure (e.g., `proj_dir/app_name.py`) 
into a more standard one (e.g., `proj_dir/app_name/app_name.py`) for building 
with `poetry build`. 

The script moves the app files from the root project directory into a sub-directory 
named after the app (as specified in the `pyproject.toml` file), leaving the 
meta files (e.g., `README.md`, `LICENSE`, `pyproject.toml`) in the root 
directory.

# Installation

Install with `pip` using
```bash
pip install poetry-org
```

# Usage

Run in the root directory of the poetry project (where `pyproject.toml` is located). 
```bash
poetry-org
```