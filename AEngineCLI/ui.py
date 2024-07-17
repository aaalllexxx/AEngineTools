import keyboard
from events import EventListener, EventTypes
from uuid import uuid4
import time
from hashlib import sha256

class Element():
    hash = ""
    color = (255, 255, 255)
    active_color = (255, 0, 0)
    position = [0, 0]
    selectable=True
    text = ""
    def __init__(self):
        self.id = uuid4().hex
    
    def set_text(self, text):
        self.text = text
    
    def to_visual(self):
        string = self.to_string()
        string = string if not string.startswith("[") else "\\" + string
        return f"[rgb({self.color[0]},{self.color[1]},{self.color[2]})]{string}[/rgb({self.color[0]},{self.color[1]},{self.color[2]})]"
    
    @property
    def hash(self):
        return sha256(f"{self.__dict__}".encode("utf-8")).digest
    
    @property
    def length(self):
        return len(self.to_string())
    
    def to_string(self):
        return self.text
    

class Label(Element):
    def __init__(self, text="Label", position=None, color=(255, 255, 255)):
        super().__init__()
        if position is None:
            position = [0, 0]
        
        self.text = text
        self.position = position
        self.color = color
        self.selectable = False
        
    def to_string(self):
        return f"| {self.text} |"

    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return f"Label(id={self.id}, text='{self.text}')"


class Button(Element):
    def __init__(self, text="Button", func=lambda x: print("button"), args=None, position=None, color=(255, 255,255), triger_once=False):
        super().__init__()
        if position is None:
            position = [0, 0]
        self.text = text
        self.position = position
        self.color = color
        self.selectable = True
        self.trigger_once = triger_once
        self.triggered = False
        self.handlers = {"enter": [func, args]}        
        EventListener.add_event(self, EventTypes.enter)

    def to_string(self):
        return f"[{self.text}]"

    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return f"Button(id={self.id}, text='{self.text}')"
    
    @property
    def func(self):
        return self.handlers["enter"][0]
    
    @func.setter
    def func(self, value):
        self.handlers["enter"][0] = value
        
    @property
    def args(self):
        return self.handlers["enter"][1]
    
    @func.setter
    def args(self, value):
        self.handlers["enter"][1] = value
        
class Input(Element):
    def __init__(self) -> None:
        super().__init__()
        self.handlers = {
            "select": [self.read, None]
        }
        self.trig = False
        EventListener.add_event(self, EventTypes.select)
    
    def to_string(self):
        data = f"|> {self.text}"
        if len(data) < 20:
            data = data + " " * (18 - len(data))
        return data +" |"
    
    def read(self, *_):
        inp = keyboard.get_hotkey_name()
        data= inp.split("+")[-1]
        if inp and not self.trig:
            if data not in list(keyboard.all_modifiers) + ["up", "down", "left", "right", "tab", "enter"]:
                if data == "backspace":
                    self.text = self.text[:-1]
                    time.sleep(0.07)
                    return
                elif data == "space":
                    data = " "
                self.text += data
                self.trig = True
        elif not inp:
            self.trig = False
    
    