import inspect
import os


celltypes = {}

for mfile in os.listdir(os.path.dirname(__file__)):
    if mfile[-3:] == '.py' and mfile[:-3] not in ('__init__', 'cell'):
        # import module and add all its classes into celltypes
        module = __import__(mfile[:-3], globals())
        celltypes.update(dict(inspect.getmembers(module, inspect.isclass)))
