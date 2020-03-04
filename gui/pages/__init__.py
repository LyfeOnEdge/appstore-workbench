from os.path import dirname, basename, isfile, join
import glob
import importlib.util

# modules = glob.glob(join(dirname(__file__), "*.py"))
# __pages__ = [ f for f in modules if isfile(f) and not f.endswith('__init__.py')]

__pages__ = [join(dirname(__file__), "README.py"), join(dirname(__file__), "exit.py")]