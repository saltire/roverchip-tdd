import inspect
import os


spritetypes = {}

for mfile in os.listdir(os.path.dirname(__file__)):
    if mfile[-3:] == '.py':
        # import module and add all its classes into spritetypes
        module = __import__(mfile[:-3], globals())
        spritetypes.update(dict(inspect.getmembers(module, inspect.isclass)))
