PLEASE DO NOT INSTALL THIS PACKAGE, IT WILL BREAK YOUR PYTHON INTERPRETER!

The **break_my_python** package breaks the Python interpreter by using a .pth
file to execute arbitrary Python code. If you happen to install this package
you can set the FIX_PYTHON environment variable to fix your Python interpreter.

This package can be removed by running:
FIX_PYTHON=1 pip uninstall break_my_python
or
FIX_PYTHON=1 conda uninstall break_my_python
will remove this package.  If neither of these work remove the 
break_my_python.pth and break_my_python.py files from the site-packages
directory.
