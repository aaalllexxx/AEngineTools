import ui
import re
import os
import sys
import time
from handlers import *
from ast import literal_eval
from storage import GlobalStorage

class Parser:
    
    @classmethod
    def parse(cls, filename: str):  
        objects = []
        sp_handlers: dict[str, Handler] = {"import": ImportHandler()}
        sp_attrs_handlers: dict[str, Handler] = {}
        specials: list[str] = list(sp_handlers)
        special_attrs: list[str] = list(sp_attrs_handlers)
        with open(filename) as file:
            data = file.read()
        
        data = " ".join(data.strip("<>").replace("\n", " ").replace("\t", " ").split()).replace(", ", ",").split("> <")
        for line in data:
            line = line.strip("<>")
            line_joined = ""
            quoted = False
            for let in line:
                if let == '"' or let == "'":
                    quoted = not quoted
                if let == " " and quoted:
                    line_joined += "$(spc)"
                else:
                    line_joined += let
            line = line_joined
            element, *args = line.split()
            if element not in specials:
                instance = getattr(ui, element)()
            else:
                instance = sp_handlers[element]
            for arg in args:
                arg = "".join(arg.split()).split("=")
                if len(arg) > 1:
                    if ('"' not in arg[1] and "'" not in arg[1]) and not arg[0] in special_attrs:
                        if re.match(r".*\$\{.*\}.*", arg[1]):
                            a = arg[1].strip("${}").split(".")
                            start = a.pop(0)
                            if start == "this":
                                GlobalStorage.this = import_module(sys.modules["__main__"].__file__.split(os.sep)[-1].split(".")[0])
                            root = getattr(GlobalStorage, start)
                            for el in a:
                                if re.match(r".*\[.*\]", el):
                                    el = el.replace("\\[", "$(esc_brack)")
                                    splited = el.split("[")
                                    
                                    varname= splited[0]
                                    root = getattr(root, varname)
                                    indicies = el.split("[", maxsplit=1)[1].split("][")
                                    for i in indicies:
                                        i = i.replace("$(esc_brack)", "[").strip("]")
                                        if '"' in i or "'" in i:
                                            root = root[i.strip("'").strip('"')]
                                        elif i.isdigit():
                                            root = root[int(i)]
                                else:
                                    root = getattr(root, el)
                            arg[1] = root
                        try:
                            setattr(instance, arg[0], literal_eval(arg[1]) if isinstance(arg[1], str) else arg[1])
                        except ValueError:
                            setattr(instance, arg[0], arg[1])
                    elif arg[0] in special_attrs:
                        sp_attrs_handlers[arg[0]].args.append(arg[1])
                        setattr(instance, arg[0], sp_attrs_handlers[arg[0]]())
                    else:
                        setattr(instance, arg[0], " ".join(arg[1].strip('"').split("$(spc)")))
                elif hasattr(instance, "args"):
                    instance.args.append(arg[0])
                
            if element in specials:
                sp_handlers[element]()
            if isinstance(instance, ui.Element):
                objects.append(instance)   
        return objects

if __name__ == "__main__":
    for d in Parser.parse("test.xml"):
        print(d)