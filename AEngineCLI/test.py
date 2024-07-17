from display import Display
import keyboard
from ui import *
from app import App

class TestApp(App):
    def __init__(self, title="AEngine App") -> None:
        super().__init__(title)
        self.fps = 150
        
    def change_label(self, *_):
        self.UI[0].set_text(self.UI[-1].text)
    
    def on_awake(self):
        self.from_aml("test.xml")

    
    def on_start(self, context: dict):
        self.display.hide_cursor()
        self.show_ui()
        
    def on_update(self, context: dict):
        if keyboard.get_hotkey_name():
            self.display.clear()
            self.show_ui()        
            
    def on_stop(self, context: dict):
        self.display.show_cursor()
 
app = TestApp()
app.run()