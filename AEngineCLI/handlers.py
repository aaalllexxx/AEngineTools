from importlib import import_module
from storage import GlobalStorage


class Handler:
    args=[]
    kwargs = {}

class ImportHandler(Handler):
    modules = {}
    def __call__(self):
        arg = self.args.pop(0)
        setattr(GlobalStorage, arg, import_module(arg))
    