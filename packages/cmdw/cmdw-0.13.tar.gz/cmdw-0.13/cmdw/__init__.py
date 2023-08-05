import imp
ROOT = os.path.dirname(os.path.dirname(__file__))
version = imp.load_source('version', os.path.join(ROOT, "__version__.py"))
__version__ 	= version.version
__email__		= "licface@yahoo.com"
__author__		= "licface@yahoo.com"

from cmdw import *