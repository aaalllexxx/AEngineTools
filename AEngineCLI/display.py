import subprocess 
import cursor
import sys
import keyboard
st_print = print
from rich import print
clear = lambda: subprocess.call('cls||clear', shell=True)


class Display:
    def __init__(self, size=[], hide_cursor=False):
        self.size = size
        self.__display: list[list[str]] = [[" " for _ in range(size[0] - 1)] for _ in range(size[1] - 1)]
        if hide_cursor:
            cursor.hide()
    
    def resize(self, x, y):
        if len(self.__display[0]) < x:
            for i, el in enumerate(self.__display):
                self.__display[i] += [" " for _ in range(x - len(self.__display[0]))] 
        else:
            for i, el in enumerate(self.__display):
                self.__display[i] = self.__display[i][:x]
        
        if len(self.__display) < y:
            for i in range(x - len(self.__display)):
                self.__display.append([" " for _ in range(x)])
        else:
            self.__display = self.__display[:y]
        
        self.size = [x, y]
    
    def show(self):
        result = ""
        for el in self.__display:
            result += "".join(el) + "\n"
        result = result[:-1]
        sys.stdout.flush()
        print(result + "\r")
    
    def bind(self, item, align=None):
        data = item.to_visual()
        space_length = 0
        if align == "center":
            space_length = self.size[0] // 2 - item.length // 2
        elif align == "right":
            space_length = self.size[0] - item.length
        else:
            space_length = item.position[0]
        
        self.__display[item.position[1]][item.position[0] or space_length] = data

    
    def clear(self):
        clear()
        self.__display: list[list[str]] = [[" " for _ in range(self.size[0] - 1)] for _ in range(self.size[1] - 1)]
    
    def __getitem__(self, index):
        return self.__display[index]
    
    def __repr__(self):
        result = "Display(\n"
        for i in self.__display:
            result += f"{i}\n"
        return result + ")"
    
    def hide_cursor(self):
        cursor.hide()
        
    def show_cursor(self):
        cursor.show()

if __name__ == "__main__":
    disp = Display([10, 10])
    disp.show()