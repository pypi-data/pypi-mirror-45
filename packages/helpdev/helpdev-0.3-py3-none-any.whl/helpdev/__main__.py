#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""HelpDev - Extracts information about the Python environment (hardware, OS, distribution, packages, paths, etc).

Authors:
    - Daniel Cosmo Pizetta <daniel.pizetta@usp.br>

Since:
    2019/04/16

License:
    MIT

"""


import argparse
import sys

import helpdev


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__.split("\n")[0])

    parser.add_argument('--hardware', action='store_true',
                        help="CPU, memory and architecture (PEI)")
    parser.add_argument('--os', action='store_true',
                        help="Operating system (PEI)")
    parser.add_argument('--thread', action='store_true',
                        help="Threads specification in the system (PEI)")
    parser.add_argument('--network', nargs='?', default=10, type=int,
                        help="Network information, DNS and load for usual sites (PEI)"
                             "NETWORK timeout defaults to 10s. 0 is disabled.")
    parser.add_argument('--python', action='store_true',
                        help="Python distribution (PED)")
    parser.add_argument('--conda', action='store_true',
                        help="Conda/Anaconda Python distribution (PED)")
    parser.add_argument('--qt', action='store_true',
                        help="All about Qt, abstractions (QtPy/Qt.Py/PyQtGraph), "
                             "bindings (PyQt/PySide) and Qt (C++)(PEAD)")

    parser.add_argument('--packages', action='store_true',
                        help="All options of packages below (PED)")
    parser.add_argument('--packages-pip', action='store_true',
                        help="PIP installed packages + PIP check (PED)")
    parser.add_argument('--packages-pip-e', action='store_true',
                        help="PIP locally installed packages + PIP check (PED)")
    parser.add_argument('--packages-conda', action='store_true',
                        help="CONDA installed packages (PED)")
    parser.add_argument('--packages-conda-e', action='store_true',
                        help="CONDA locally installed packages (PED)")

    parser.add_argument('--numbers', action='store_true',
                        help="All options above, 'float' and 'int' (PEI)")
    parser.add_argument('--float', action='store_true',
                        help="Float representation in the system (PEI)")
    parser.add_argument('--int', action='store_true',
                        help="Integer representation in the system (PEI)")

    # this may contains personal folder adresses, be carefull sharing
    parser.add_argument('--personal', action='store_true',
                        help="All options below, 'path' and 'scope' (PEAD)")
    parser.add_argument('--path', action='store_true',
                        help="Show Python current paths i.e. 'sys.path' (PEAD)")
    parser.add_argument('--scope', action='store_true',
                        help="Show Python current scope i.e. 'dir()' (PEAD)")

    parser.add_argument('--all', action='store_true',
                        help="Run all options, except 'personal' (PEAD)")
    parser.add_argument('--all-for-sure', action='store_true',
                        help="Run all options, INCLUDING 'PERSONAL' "
                             "folder paths and information (PEAD)")

    parser.add_argument('--version', '-v', action='version',
                        version='v{}'.format(helpdev.__version__))

    arguments = parser.parse_args()

    return arguments


def main():
    """Main function."""
    args = parse_args()

    info = {}

    # To not repeat the test
    if args.all_for_sure:
        args.all = True

    no_args = not len(sys.argv) > 1

    # Common information
    if args.hardware or args.all or no_args:
        info.update(helpdev.check_hardware())
    if args.os or args.all or no_args:
        info.update(helpdev.check_os())
    if args.thread or args.all or no_args:
        info.update(helpdev.check_thread())
    if args.all or no_args:
        info.update(helpdev.check_network(args.network))

    # Also common and important information
    if args.python or args.all or no_args:
        info.update(helpdev.check_python())
    if args.conda or args.all or no_args:
        info.update(helpdev.check_conda())
    if args.qt or args.all or no_args:
        info.update(helpdev.check_qt_abstractions())
        info.update(helpdev.check_qt_bindings())

    if args.float or args.all or args.numbers:
        info.update(helpdev.check_float())
    if args.int or args.all or args.numbers:
        info.update(helpdev.check_int())

    # From PIP and Conda
    if args.packages_pip or args.all or args.packages:
        info.update(helpdev.check_python_packages())
    if args.packages_pip_e:
        info.update(helpdev.check_python_packages(edit_mode=True))
    if args.packages_conda or args.all or args.packages:
        info.update(helpdev.check_conda_packages())
    if args.packages_conda_e or args.all:
        info.update(helpdev.check_conda_packages(edit_mode=True))

    # Personal information for self-check, not executed when --all is passed
    if args.path or args.all_for_sure or args.personal:
        info.update(helpdev.check_path())
    if args.scope or args.all_for_sure or args.personal:
        info.update(helpdev.check_scope())

    for key, dict_info in info.items():
        print('* {:-<110}'.format(key))
        for key, value in dict_info.items():
            print('    - {:.<30} {}'.format(key, value))
