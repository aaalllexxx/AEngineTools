import keyboard

class EventTypes:
    enter: str = "enter"
    change: str = "change"
    select: str = "select"
    unselect: str = "unselect"

class EventListener:
    __instance = None
    view_items = {}
    states = {}
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(EventListener, cls).__new__(cls)
        return cls.__instance
        
    @classmethod
    def add_event(cls, element, event_type):
        if not event_type in cls.view_items:
            cls.view_items[event_type] = []
        cls.view_items[event_type].append(element)
        cls.states[element] = element.hash
    
    @classmethod
    def listen(cls, context: dict):
        active_element = context.get("active_element")
        if active_element.selectable:
            if cls.view_items.get(EventTypes.select) and active_element in cls.view_items[EventTypes.select] and active_element.handlers.get("select"):
                f = active_element.handlers.get("select")
                if f:
                    f[0](f[1])
            if cls.view_items.get(EventTypes.enter) and active_element in cls.view_items[EventTypes.enter] and keyboard.is_pressed("enter") and (not active_element.triggered or not active_element.trigger_once):
                if active_element.handlers.get("enter"):
                    f = active_element.handlers.get("enter")
                    if f:
                        active_element.triggered = True
                        f[0](f[1])
            elif not keyboard.is_pressed("enter"):
                active_element.triggered = False
            if cls.view_items.get(EventTypes.change) and active_element in cls.view_items[EventTypes.change] and active_element.hash != cls.states[active_element]:
                if active_element.get("change"):
                    f = active_element.handlers.get("change")
                    if f:
                        f[0](f[1])
            
        
    