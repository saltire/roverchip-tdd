import inspect
import os


leveltypes = {}

for mfile in os.listdir(os.path.dirname(__file__)):
    if mfile != '__init__.py' and mfile[-3:] == '.py' and mfile[:-3] != 'level':
        # import module and add all its classes into leveltypes
        module = __import__(mfile[:-3], globals())
        leveltypes.update(dict(inspect.getmembers(module, inspect.isclass)))
