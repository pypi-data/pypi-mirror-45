#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""HelpDev - Extract information about the hardware, OS, Python distributions and packages.

Important:
    Some of the information here are set at runtime. So, you need to keep your
    applications running and run this script at the same time and, of course, at
    the same Python environment. You must run it inside your running Python environment
    along with the application you would report something! To be used from Python 3.4+.

        - PEI: Python environment independent.
        - PED: Python environment DEPENDENT.
        - PEAD: Python environment and application DEPENDENT.

Note:
    This script is not supposed to get personal information, however you must
    check the information before using the output.

This code is based on many other scripts from:

   - zhreshold <https://gist.github.com/zhreshold/f4defab409cc0e6f6a0e75237f73ca99>
   - QDarkStyle <>
   - QtPy <>

Authors:
    - Daniel Cosmo Pizetta <daniel.pizetta@usp.br>

Since:
    2019/04/16

License:
    MIT

"""

__version__ = "0.1"


import copy
import importlib.util
import os
import platform
import socket
import subprocess
import sys
import time
import warnings

import psutil

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen


QT_BINDINGS = ['PyQt4', 'PyQt5', 'PySide', 'PySide2']
"""list: values of all Qt bindings to import."""

QT_ABSTRACTIONS = ['qtpy', 'pyqtgraph', 'Qt']
"""list: values of all Qt abstraction layers to import."""

URLS = {
    'PyPI': 'https://pypi.python.org/pypi/pip',
    'Conda': 'https://repo.continuum.io/pkgs/free/',
    'GitLab': 'https://gitlab.com',
    'GitHub': 'https://github.com',
    'Google': 'https://google.com'
}



def check_constants():
    """Check basic constants values."""


def check_float():
    """Check float limits information.

    Get information from ``sys`` library.
    """

    info = {'FLOAT':
            {'Epsilon': sys.float_info.epsilon,
             'Digits': sys.float_info.dig,
             'Precision': sys.float_info.mant_dig,
             'Maximum': sys.float_info.max,
             'Maximum Exp.': sys.float_info.max_exp,
             'Max. 10 Exp.': sys.float_info.max_10_exp,
             'Minimum': sys.float_info.min,
             'Miminim Exp.': sys.float_info.min_exp,
             'Min. 10 Exp.': sys.float_info.min_10_exp,
             'Radix': sys.float_info.radix,
             'Rounds': sys.float_info.rounds
             }
            }

    return info


def check_int():
    """Check int limits information.

    Get information from ``sys`` library.
    """

    info = {'INTEGER':
            {'Bits per Digit': sys.int_info.bits_per_digit,
             'Size of Digit': sys.int_info.sizeof_digit
             }
            }

    return info


def check_python():
    """Check Python information.

    It is Python environment dependent.
    """

    info = {'PYTHON DISTRIBUTION':
            {'Version': platform.python_version(),
             'Compiler': platform.python_compiler(),
             'Build': platform.python_build()[0] + ' of ' + platform.python_build()[1],
             'Implem.': platform.python_implementation(),
             'API': sys.api_version
             }
            }

    return info


def check_python_packages(edit_mode=False):
    """Check PIP installed packages."""

    all_packages = ''

    if edit_mode:
        all_packages = str(subprocess.check_output('pip list -e',
                                                   shell=True), 'utf-8').strip()
    else:
        # list all packages, including in editable mode
        all_packages = str(subprocess.check_output('pip list',
                                                   shell=True), 'utf-8').strip()

    # split lines and remove table name
    line_packages = all_packages.split("\n")[2:]

    info = {'PYTHON PACKAGES (pip list)': {}}

    # clean spaces, create a list and insert in the dictionary
    for line in line_packages:
        splitted = line.split(' ')
        cleaned = ' '.join(splitted).split()
        info['PYTHON PACKAGES (pip list)'][cleaned[0]] = cleaned[1]

    return info


def check_conda():
    """Check Conda Python distribution information.

    It is Python/Conda environment dependent.
    """

    info = {'CONDA DISTRIBUTION': {}}

    all_info = str(subprocess.check_output('conda info',
                                           shell=True), 'utf-8').strip()

    for line in all_info.split("\n"):
        if "conda version : " in line:
            info['CONDA DISTRIBUTION']['Version'] = line.split(" : ")[1]
        elif "conda-build version : " in line:
            info['CONDA DISTRIBUTION']['Build'] = line.split(" : ")[1]
        elif "python version : " in line:
            info['CONDA DISTRIBUTION']['Python'] = line.split(" : ")[1]

    return info


def check_conda_packages(edit_mode=False):
    """Check conda inslalled packages information.

    It is Python/Conda environment dependent.
    """

    info = {'CONDA PACKAGES (conda)': {}}

    # skip first 3 lines
    line_packages = str(subprocess.check_output('conda list --export',
                                                shell=True).decode('utf-8')).strip()[2:]

    for line in line_packages:
        if not "pypi" and "dev" not in line:
            splitted = line.split('=')
            info['CONDA PACKAGES'][splitted[0]] = splitted[1]

    return info


def check_hardware():
    """Check hardware information.

    It uses subprocess commands for each system along with psutil library.
    So you need to install psutil library.
    """

    cpu = ''

    # mac
    if sys.platform.startswith('darwin'):
        all_info = str(subprocess.check_output(['sysctl -a'],
                                               shell=True), 'utf-8').strip()
        for line in all_info.split("\n"):
            if "brand_string" in line:
                cpu = line.split(": ")[1]
                break
    # linux
    elif sys.platform.startswith('linux'):
        all_info = str(subprocess.check_output('lscpu',
                                               shell=True), 'utf-8').strip()
        for line in all_info.split("\n"):
            if "Model name:" in line:
                cpu = line.split(':')[1]
                break
    # windows
    elif sys.platform.startswith('win32'):
        all_info = str(subprocess.check_output(['wmic', 'cpu', 'get', 'name'],
                                               shell=True), 'utf-8').strip()
        if "Name" in all_info:
            cpu = all_info.replace('Name', '')
    try:
        mem = str(int(psutil.virtual_memory().total / 1000000)) + " MB"
        mem_used = str(int(psutil.virtual_memory().total / 1000000)) + " MB"
    except ImportError:
        mem = 'psutil library not available'
        mem_used = mem

    info = {'HARDWARE':
            {'Machine': platform.machine(),
             'Processor': cpu.lstrip(),
             'Memory': mem,
             'Used memory': mem_used
             }
            }

    return info


def check_os():
    """Check operating system information."""

    info = {'OPERATING SYSTEM':
            {'System': platform.system(),
             'Release': platform.release(),
             'Platform': platform.platform(),
             'Version': platform.version()
             }
            }

    return info


def check_network(timeout):
    """Check network connection for URLS list with timeout."""

    info = {'NETWORK':
            {'Timeout': timeout
             }
            }

    if timeout > 0:
        socket.setdefaulttimeout(timeout)

    for name, url in URLS.items():
        urlinfo = urlparse(url)
        error = False

        # DNS
        dns_err = ''
        start = time.time()
        try:
            _ = socket.gethostbyname(urlinfo.netloc)
        except Exception as err:  # analysis:ignore
            dns_err = str(err)
            info['NETWORK'][name] = "DNS ERROR: {}s URL: {}".format(dns_err, url)
            error = True
        dns_elapsed = time.time() - start

        # LOAD
        load_err = ''
        start = time.time()
        try:
            _ = urlopen(url, timeout=timeout)
        except Exception as err:  # analysis:ignore
            load_err = str(err)
            info['NETWORK'][name] = "LOAD ERROR: {}s URL: {}".format(load_err, url)
            error = True
        load_elapsed = time.time() - start

        if not error:
            info['NETWORK'][name] = "DNS: {:.4f}s LOAD: {:.4f}s URL: {}".format(dns_elapsed,
                                                                                load_elapsed,
                                                                                url)

    return info


def check_qt_bindings():
    """Check all Qt bindings related information."""

    info = {'QT BINDINGS': {}}

    for binding in installed_qt_bindings():
        api, qt = qt_binding_information(binding)
        info['QT BINDINGS'][binding + ' Version'] = api
        info['QT BINDINGS'][binding + ' Qt Version'] = qt

    return info


def check_qt_abstractions():
    """Check all Qt abstractions related information."""

    info = {'QT ABSTRACTIONS': {}}

    for abstraction in installed_qt_abstractions():
        api, qt = qt_abstraction_information(abstraction)
        info['QT ABSTRACTIONS'][abstraction + ' Version'] = api
        info['QT ABSTRACTIONS'][abstraction + ' Binding'] = qt

    return info


def installed_qt_bindings():
    """Return a list of qt bindings available."""
    return check_installed(import_list=QT_BINDINGS)


def installed_qt_abstractions():
    """Return a list of qt abstraction layers available."""
    return check_installed(import_list=QT_ABSTRACTIONS)


def check_installed(import_list):
    """Return a list of installed packages from import_list."""

    # Disable warnings here
    warnings.filterwarnings("ignore")

    import_list_return = copy.deepcopy(import_list)
    # Using import_list_return var in for, does not work in py2.7
    # when removing the element, it reflects on for list
    # so it skips next element
    for current_import in import_list:

        spec = True
        # Copy the sys path to make sure to not insert anything
        sys_path = sys.path

        # Check import
        if sys.version_info >= (3, 4):
            spec = importlib.util.find_spec(current_import)
        else:
            try:
                __import__(current_import)
            except RuntimeWarning:
                spec = True
            except Exception:
                spec = None
            else:
                spec = True

        if spec is None:
            # Remove if not available
            import_list_return.remove(current_import)

        # Restore sys path
        sys.path = sys_path

    # Restore warnings
    warnings.resetwarnings()

    return import_list_return


def qt_abstraction_information(import_name):
    """Get abstraction layer version and binding (default or current if in use)."""

    # copy sys.path
    sys_path = sys.path
    api_version = ''
    env_var = ''

    if import_name == 'pyqtgraph':
        try:
            from pyqtgraph import __version__ as api_version  # analysis:ignore
            if 'PYQTGRAPH_QT_LIB' not in os.environ:
                env_var = 'Not set or inexistent'
            else:
                env_var = os.environ['PYQTGRAPH_QT_LIB']
        except ImportError:
            raise ImportError('PyQtGraph cannot be imported.')

    elif import_name == 'qtpy':
        try:
            from qtpy import __version__ as api_version  # analysis:ignore
            if 'QT_API' not in os.environ:
                env_var = 'Not set or inexistent'
            else:
                env_var = os.environ['QT_API']
        except ImportError:
            raise ImportError('QtPy cannot be imported.')

    elif import_name == 'Qt':
        try:
            from Qt import __version__ as api_version  # analysis:ignore
            from Qt import __binding__ as env_var  # analysis:ignore
        except ImportError:
            raise ImportError('Qt.py cannot be imported.')
    else:
        return ('', '')

    # restore sys.path
    sys.path = sys_path

    return (api_version, env_var)


def qt_binding_information(import_name):
    """Get binding information of version and Qt version.

    ``import_name`` is an importing name, case sensitive.
    """

    # copy sys.path
    sys_path = sys.path

    if import_name == 'PyQt4':
        try:
            from PyQt4.Qt import PYQT_VERSION_STR as api_version  # analysis:ignore
            from PyQt4.Qt import QT_VERSION_STR as qt_version  # analysis:ignore
        except ImportError:
            raise ImportError('PyQt4 cannot be imported.')

    elif import_name == 'PyQt5':
        try:
            from PyQt5.QtCore import PYQT_VERSION_STR as api_version  # analysis:ignore
            from PyQt5.QtCore import QT_VERSION_STR as qt_version  # analysis:ignore
        except ImportError:
            raise ImportError('PyQt5 cannot be imported.')

    elif import_name == 'PySide':
        try:
            from PySide import __version__ as api_version  # analysis:ignore
            from PySide.QtCore import __version__ as qt_version  # analysis:ignore
        except ImportError:
            raise ImportError('PySide cannot be imported.')

    elif import_name == 'PySide2':
        try:
            from PySide2 import __version__ as api_version  # analysis:ignore
            from PySide2.QtCore import __version__ as qt_version  # analysis:ignore
        except ImportError:
            raise ImportError('PySide2 cannot be imported.')
    else:
        return ('', '')

    # restore sys.path
    sys.path = sys_path

    return (api_version, qt_version)


def check_path():
    """Check Python path or sys.path"""

    info = {'SYS.PATH': {}}

    for num, path in enumerate(sys.path):
        info['SYS.PATH'][num] = path

    return info


def check_scope():
    """Check Python scope or dir()"""

    info = {'SCOPE': {}}

    for num, path in enumerate(dir()):
        info['SCOPE'][num] = path

    return info
