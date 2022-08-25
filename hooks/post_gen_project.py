import os
import shutil

use_react = '{{cookiecutter.use_react}}' == 'y'

if not use_react:
    # Drop the react folder
    path = os.path.join(os.getcwd(), '{{cookiecutter.app_name}}/static/react')
    shutil.rmtree(path)
