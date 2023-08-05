from pathlib import Path
import toml
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s :: %(message)s')


def main():
    try:
        toml_data = toml.load('pyproject.toml', _dict=dict)
    except FileNotFoundError as e:
        logging.error('Poetry TOML file not found. \n         ' \
            'Run poetry_org in the Poetry project root directory.')
        return

    app_name = toml_data['tool']['poetry']['name'].replace('-','_')
    app_version = toml_data['tool']['poetry']['version']
    app_name_hyphens = app_name.replace('_','-')

    exclude_files = [ 'pyproject.toml',
                      'poetry.lock',
                      'requirements.txt',
                      'readme.md',
                      'readme.rst',
                      'license',
                      '.gitignore',
                      '__pycache__',
                      '.pytest_cache',
                      'dist',
                      app_name + '.egg-info',
                      'tests',
                      app_name,
                      'demo_' + app_name
                    ]


    proj_dir = Path.cwd()

    '''Make app directory'''
    app_dir = proj_dir / app_name
    app_dir.mkdir(parents=True, exist_ok=True)

    '''Copy app .py files into app directory'''
    py_files = proj_dir.glob('*.py')
    for file in py_files:
        if '-' in file.name:
            orig_filename = file.name
            file.rename(file.parent / file.name.replace('-','_'))
            logging.warning(f'Renamed {orig_filename}.py to {file.name}.py')
    py_files = proj_dir.glob('*.py')
    copy(items=py_files, to_directory=app_dir)

    '''Copy other files to a demo directory'''
    remaining_files = proj_dir.glob('*')
    demo_dir = proj_dir / (f'demo_' + app_name)
    demo_dir.mkdir(parents=True, exist_ok=True)
    copy(items=remaining_files, to_directory=demo_dir, exclude=exclude_files)
    demo_app_file = demo_dir / (f'demo_' + app_name + '.py')
    if not demo_app_file.exists():
        demo_app_file.write_text(f'import {app_name}\n\n')

    '''Create app __init__ file'''
    pyfiles = app_dir.glob('*.py')
    init_file = app_dir / '__init__.py'
    init_imports = [f"__version__ = \'{app_version}\'\n"]
    for pyfile in pyfiles:
        if pyfile.name != '__init__.py':
            init_imports.append('from .' + pyfile.stem + ' import *')
    init_file.write_text('\n'.join(init_imports))
    logging.info(f'Updated file __init__.py in ./{app_name}/')

    '''Add test directory if not there.'''
    test_dir = proj_dir / 'tests'
    test_dir.mkdir(parents=True, exist_ok=True)
    test_init_file = Path(test_dir, '__init__.py')
    test_dir_update = False
    if not test_init_file.exists():
        test_init_file.write_text('')
        test_dir_update = True
    test_app_file = Path(test_dir, f'test_{app_name}.py')
    if not test_app_file.exists():
        test_app_file.write_text(f'from {app_name} import __version__\n\n\n'
        f'def test_version():\n'\
        f'    assert __version__ == \'{app_version}\'')
        test_dir_update = True
    if test_dir_update:
        logging.info(f'Updated ./tests/ directory.')


    logging.info(f'Success! File structure of app {app_name} is ready for `poetry build`.\n')
    return

def copy(items, to_directory, exclude=[]):
    for item in items:
        if not item.name.lower() in exclude and not item.name.startswith('.'):
            new_item_path = to_directory/item.name
            logging.info(f'Moving   ./{item.name}  -->  ./{to_directory.name}/{item.name}')
            if new_item_path.exists():
                logging.error(f'File {new_item_path} already exists!\n ** Merge files and re-run script. **')
                return
            item.replace(new_item_path)

if __name__ == '__main__':
    main()
