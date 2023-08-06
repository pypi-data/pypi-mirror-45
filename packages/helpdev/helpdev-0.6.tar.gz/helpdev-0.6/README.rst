HelpDev
=======

Helping users and developers to get information about the environment to
report bugs or even test your system without spending a day on it. It can
get information about hardware, OS, paths, Python distribution and packages,
including Qt-things. Operates in Linux, Windows and Mac. You must run it
inside your running Python environment along with the application you would
report something or test!

If you want to get information at runtime of your application, you need
to call using the same environment (and process) in which your application
is running. This module can be imported and integrated into your application,
providing a report about the current environment.

Some information can be depedent or independent of your Python environment,
and some others can be dependent your running application. So, there are some
acronymn used to refer to them:

- PEI: Python environment independent;

- PED: Python environment DEPENDENT;

- PEAD: Python environment and application DEPENDENT.


**Caution:**

- This script is not supposed to get personal information using the option
  ``--all``, but you must check the information before using the output.

- Using the option ``--all-for-sure`` it is added information about paths and
  variables that can show personal information. So, be sure when using this
  option when publishing in the web.

- I'm not responsible for bad use or problems with the information given by
  this script, but if pointed in the Issues, I can help fixing it.


Installing, updating and uninstalling
#####################################


To install and/or update, do ::

    $ pip install -U helpdev


To remove ::

    $ pip uninstall helpdev


Running
#######


You just need to run in the terminal the line(s) below.


To get a minimalist output ::

    $ helpdev


To get a complete output without personal information ::

    $ helpdev --all


To get a complete output WITH PERSONAL INFORMATION ::

    $ helpdev --all-for-sure


To get some help information ::

    $ helpdev --help


Examples from v0.6
##################


Help
----


.. code-block::

    $ helpdev --help


.. include:: examples/help.txt
   :literal:


With --packages filter
----------------------

This filtering feature provides a clean list of packages to report. It
accepts regular expressions. Each expression must be separated by comma.

The basic regular expression checks the start until the end of the package
name and they are case insenstitive.

.. code-block::

    # gets all that starts with 'sphinx'
    $ helpdev --packages="sphinx.*,qtpy,PYQT5"


.. include:: examples/filter.txt
   :literal:


With --all option
-----------------


.. code-block::

    $ helpdev --all


.. include:: examples/all.txt
   :literal:


This code is based on many other scripts from:

   - `zhreshold <https://gist.github.com/zhreshold/f4defab409cc0e6f6a0e75237f73ca99>`_
   - `QDarkStyle <https://github.com/ColinDuquesnoy/QDarkStyleSheet>`_
   - `QtPy <https://github.com/spyder-ide/qtpy>`_
