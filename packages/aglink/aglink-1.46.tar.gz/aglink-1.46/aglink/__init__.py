import imp
version = imp.load_source('version', "../__version__.py")
__version__ 	= version.version
__test__    	= '0.6'
__build__		= '2.7'
__platform__	= 'all'
__email__		= "licface@yahoo.com"

from .agl import autogeneratelink
