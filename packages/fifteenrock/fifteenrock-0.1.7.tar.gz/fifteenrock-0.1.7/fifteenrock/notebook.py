from typing import *

from IPython import get_ipython
from fifteenrock.core import deploy
from fifteenrock import helper

import nbformat
from nbconvert import PythonExporter
from pathlib import Path

from notebook.notebookapp import list_running_servers
import json
import re
import ipykernel
from urllib.parse import urlencode, urljoin
from urllib.request import urlopen
from os import path


def notebook_file_name(ikernel):
    """Return the full path of the jupyter notebook."""
    # Check that we're running under notebook
    if not (ikernel and ikernel.config['IPKernelApp']):
        return

    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for srv in servers:
        query = {'token': srv.get('token', '')}
        url = urljoin(srv['url'], 'api/sessions') + '?' + urlencode(query)
        for session in json.load(urlopen(url)):
            if session['kernel']['id'] == kernel_id:
                relative_path = session['notebook']['path']
                return path.join(srv['notebook_dir'], relative_path)


def deploy_notebook(project: str, function: str, url: str = None, dependencies: List = None,
                    credentials: Dict = None) -> None:
    if is_notebook():

        credentials = credentials or helper.determine_credentials()

        tmp_dir = Path('/Users/rabraham/tmp')

        module_path = tmp_dir / 'main.py'
        kernel = get_ipython()
        notebook_path = notebook_file_name(kernel)

        convert_notebook(notebook_path, module_path)
        result = deploy(credentials=credentials, main_file=str(module_path), project=project, function=function,
                        url=url,
                        dependencies=dependencies)
        print(result)
        return result
    else:
        print('WARNING: deploy_notebook is only executed from a notebook')
        pass


def convert_notebook(notebook_path, module_path):
    with open(notebook_path) as fh:
        nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

    exporter = PythonExporter()
    source, meta = exporter.from_notebook_node(nb)

    with open(module_path, 'w') as fh:
        fh.writelines(source)


def is_notebook():
    try:
        kernel = get_ipython()
        shell = kernel.__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter
