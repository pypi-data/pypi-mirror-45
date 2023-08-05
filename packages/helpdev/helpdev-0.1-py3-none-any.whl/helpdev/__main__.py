#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse

import helpdev


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Python environment independent
    parser.add_argument('--hardware', action='store_true',
                        help="CPU, memory and architecture (PEI)")
    parser.add_argument('--os', action='store_true',
                        help="Operating system (PEI)")
    parser.add_argument('--float', action='store_true',
                        help="Float representation in the system (PEI)")
    parser.add_argument('--int', action='store_true',
                        help="Integer representation in the system (PEI)")
    parser.add_argument('--network', action='store_true',
                        help="Network information, DNS and load for usual sites (PEI)")
    parser.add_argument('--timeout', default=10, type=int,
                        help="Connection test timeout threshold, 0 to disable (Option)")

    # Python environment dependent
    parser.add_argument('--python', action='store_true',
                        help="Python distribution (PED)")
    parser.add_argument('--conda', action='store_true',
                        help="Conda/Anaconda Python distribution (PED)")

    parser.add_argument('--python-packages', action='store_true',
                        help="PIP installed packages + PIP check (PED)")
    parser.add_argument('--python-packages-e', action='store_true',
                        help="PIP locally installed packages + PIP check (PED)")

    parser.add_argument('--conda-packages', action='store_true',
                        help="CONDA installed packages (PED)")
    parser.add_argument('--conda-packages-e', action='store_true',
                        help="CONDA locally installed packages (PED)")

    # Python environment and application dependent
    parser.add_argument('--qt', action='store_true',
                        help="All about Qt, abstractions (QtPy/Qt.Py/PyQtGraph), bindings (PyQt/PySide) and Qt (C++)(PEAD)")

    # Python environment and application dependent
    # This may contains personal folder adresses, be carefull sharing
    parser.add_argument('--path', action='store_true',
                        help="Show Python current paths i.e. sys.path (PEAD)")
    parser.add_argument('--scope', action='store_true',
                        help="Show Python current scope i.e. dir() (PEAD)")

    parser.add_argument('--all', action='store_true',
                        help="Run all options, except 'path' and 'scope'(PEAD)")
    parser.add_argument('--sure-all', action='store_true',
                        help="Run all options, INCLUDING 'path' and 'scope', personal folder paths and information (PEAD)")

    arguments = parser.parse_args()

    return arguments


def main():
    args = parse_args()

    info = {}

    # To not repeat the test
    if args.sure_all:
        args.all = True

    # Common information
    if args.hardware or args.all:
        info.update(helpdev.check_hardware())
    if args.os or args.all:
        info.update(helpdev.check_os())
    if args.float or args.all:
        info.update(helpdev.check_float())
    if args.int or args.all:
        info.update(helpdev.check_int())
    if args.network or args.all:
        info.update(helpdev.check_network(args.timeout))

    # Also common and important information
    if args.python or args.all:
        info.update(helpdev.check_python())
    if args.conda or args.all:
        info.update(helpdev.check_conda())
    if args.qt or args.all:
        info.update(helpdev.check_qt_abstractions())
        info.update(helpdev.check_qt_bindings())

    # From PIP
    if args.python_packages or args.all:
        info.update(helpdev.check_python_packages())
    if args.python_packages_e:
        info.update(helpdev.check_python_packages(edit_mode=True))

    # From Conda
    if args.conda_packages or args.all:
        info.update(helpdev.check_conda_packages())
    if args.conda_packages_e or args.all:
        info.update(helpdev.check_conda_packages(edit_mode=True))

    # Personal information for self-check, not executed when --all is passed
    if args.path or args.sure_all:
        info.update(helpdev.check_path())
    if args.scope or args.sure_all:
        info.update(helpdev.check_scope())

    for key, dict_info in info.items():
        print('* {:-<110}'.format(key))
        for key, value in dict_info.items():
            print('    - {:.<30} {}'.format(key, value))
