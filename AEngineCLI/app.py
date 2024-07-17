import shutil
import time
import keyboard
import cursor

from display import Display
from aml_parser import Parser
from os import terminal_size
from events import EventListener

class App:
    def __init__(self, title="AEngine App") -> None:
        self.title: str = title
        __size: terminal_size = shutil.get_terminal_size()
        self.size: tuple[int, int] = (__size.columns, __size.lines)
        self.fps = 10
        self.running = True
        self.context = {}
        self.display = Display([self.size[0], self.size[1]])
        self.UI = []
        self.active_index = 0
        self.hooks = list("abcdefghijklmnopqrstuvwxyz!,./?!@#$%^&*()--+= ") 
        
    def activate_next(self):
        if self.active_index < len(self.UI) - 1:
            index = self.active_index + 1
            while not self.UI[index].selectable:
                index += 1
            if index > -1 and index < len(self.UI):
                self.context["active_element"].color = self.context["initial_colors"][self.active_index]
                self.context["active_element"] = self.UI[index]
                self.context["active_element"].color = self.context["active_element"].active_color
                self.active_index = index
    
    def activate_prev(self):
        if self.active_index > 0:
            index = self.active_index - 1
            while not self.UI[index].selectable:
                index -= 1
            if index > -1 and index < len(self.UI):
                self.context["active_element"].color = self.context["initial_colors"][self.active_index]
                self.context["active_element"] = self.UI[index]
                self.context["active_element"].color = self.context["active_element"].active_color
                self.active_index = index
        
    def add_ui(self, element, align=None):
        if element not in self.UI:
            self.context["initial_colors"].append(element.color)
            self.UI.append(element)
    
    def show_ui(self):
        for el in self.UI:
            align = el.align if hasattr(el, "align") else "left"
            self.display.bind(el, align)
        self.display.show()
        
    def on_start(self, context: dict):
        pass
    
    def on_awake(self):
        pass
    
    def on_update(self, context: dict):
        pass
    
    def on_stop(self, context: dict):
        pass
    
    def __block_inner_keys(self):
        for key in self.hooks:
            keyboard.hook_key(key, lambda x: None, True)
    
    def from_aml(self, path):
        ui = Parser.parse(path)
        for element in ui:
            self.add_ui(element)
    
    def run(self):
        try:
            if "initial_colors" not in self.context:
                self.context["initial_colors"] = []
            self.on_awake()
            if "active_element" not in self.context:
                self.context["active_element"] = self.UI[0]
            keyboard.block_key("enter")
            keyboard.add_hotkey("up", self.activate_prev, suppress=True)
            keyboard.add_hotkey("down", self.activate_next, suppress=True)
            self.__block_inner_keys()
            if self.context["active_element"].selectable:
                self.context["active_element"].color = self.context["active_element"].active_color
            else:
                self.activate_next()
            self.on_start(self.context)
            while self.running:
                if keyboard.get_hotkey_name() == "ctrl+c":
                    self.running = False
                    exit()
                EventListener.listen(self.context)
                self.on_update(self.context)
                time.sleep(1 / self.fps)
            self.on_stop(self.context)
        except KeyboardInterrupt:
            exit(0)
        finally:
            self.display.clear()
            cursor.show()
            keyboard.unhook_all()
