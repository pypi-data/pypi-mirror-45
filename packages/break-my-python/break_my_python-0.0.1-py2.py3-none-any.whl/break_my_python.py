from __future__ import print_function
import sys
import os
fixed = 'FIX_PYTHON' in os.environ
pth_file = __file__
message = """
Your python is broken, sorry :(
Setting the FIX_PYTHON environment variable will allow python to run again.
You can remove break_my_python by running:
FIX_PYTHON=1 pip uninstall break_my_python
or
FIX_PYTHON=1 conda remove break_my_python
"""
if not fixed:
    print(message)
    sys.exit(42)
