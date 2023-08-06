import imp
version = imp.load_source('version', "../__version__.py")
print version.version