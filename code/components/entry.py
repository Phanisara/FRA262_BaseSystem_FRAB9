import platform
import re
import tkinter as tk
from components.color import Color
from components.shape import RoundRectangle

class OrderEntry():
    def __init__(self, master, canvas, x, y, w, h, color):
        self.master = master
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.string_var = tk.StringVar() 
        self.outer_rec = RoundRectangle(canvas=self.canvas, x=self.x, y=self.y, w=self.w, h=self.h, r=4, color=self.color)
        self.inner_rec = RoundRectangle(canvas=self.canvas, x=self.x+2, y=self.y+2, w=self.w-4, h=self.h-4, r=2, color=Color.whitegray)
        self.os = platform.platform()[0].upper()
        if self.os == 'M':  # Mac
            self.entry = tk.Entry(master=self.master, bg=Color.whitegray, bd=0, font="Inter-SemiBold", fg=self.color, selectforeground=self.color, highlightthickness=0, insertbackground=self.color, insertwidth=2, justify="center", width=8, textvariable=self.string_var, validate="key", validatecommand=(self.canvas.register(self.validate_number),
        '%P', '%S'))
        elif self.os == 'W':  # Windows
            self.entry = tk.Entry(master=self.master, bg=Color.whitegray, bd=0, font=("Inter SemiBold", 9), fg=self.color, selectforeground=self.color, highlightthickness=0, insertbackground=self.color, insertwidth=2, justify="center", width=8, textvariable=self.string_var, validate="key", validatecommand=(self.canvas.register(self.validate_number),
        '%P', '%S'))
        self.entry_window = self.canvas.create_window(self.x+(self.w/2), self.y+(self.h/2), window=self.entry)
        self.entry.bind("<Configure>", self.entry.config(width=self.w // 10))
        self.set_text("0")
    
    def validate_number(self, current_value, new_value):
        return new_value.isdigit() and len(str(current_value)) < 2
    
    def hide(self):
        self.outer_rec.hide()
        self.inner_rec.hide()
        self.canvas.itemconfigure(self.entry_window, state='hidden')

    def show(self):
        self.outer_rec.show()
        self.inner_rec.show()
        self.canvas.itemconfigure(self.entry_window, state='normal')

    def error(self):
        self.entry.config({ "fg": Color.red, "selectforeground": Color.red, "insertbackground": Color.red })

    def normal(self):
        self.entry.config({ "fg": self.color, "selectforeground": self.color, "insertbackground": self.color })

    def disable(self):
        self.entry.config({ "state": "disabled" })
    
    def enable(self):
        self.entry.config({ "state": "normal" })

    def set_text(self, text):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(text))

    def get_value(self):
        return self.entry.get()

class Entry():
    def __init__(self, master, canvas, x, y, w, h, color):
        self.master = master
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.string_var = tk.StringVar() 
        self.placeholder = '0'
        self.outer_rec = RoundRectangle(canvas=self.canvas, x=self.x,   y=self.y,   w=self.w, h=self.h, r=12, color=Color.gray)
        self.inner_rec = RoundRectangle(canvas=self.canvas, x=self.x+2, y=self.y+2, w=self.w-4, h=self.h-4, r=10, color=Color.whitegray)
        self.os = platform.platform()[0].upper()
        if self.os == 'M':  # Mac
            self.entry = tk.Entry(master=self.master, bg=Color.whitegray, bd=0, font="Inter-SemiBold", fg=self.color, selectforeground=self.color, highlightthickness=0, insertbackground=self.color, insertwidth=2, justify="center", width=8, textvariable=self.string_var, validate="key", validatecommand=(self.canvas.register(self.validate_number),
        '%P', '%S'))
        elif self.os == 'W':  # Windows
            self.entry = tk.Entry(master=self.master, bg=Color.whitegray, bd=0, font=("Inter SemiBold", 9), fg=self.color, selectforeground=self.color, highlightthickness=0, insertbackground=self.color, insertwidth=2, justify="center", width=8, textvariable=self.string_var, validate="key", validatecommand=(self.canvas.register(self.validate_number),
        '%P', '%S'))
        self.entry_window = self.canvas.create_window(self.x+(self.w/2), self.y+(self.h/2), window=self.entry)
        self.set_text("0")
    
    def validate_number(self, current_value, new_value):
        return new_value.isdigit() and len(str(current_value)) < 4

    def hide(self):
        self.outer_rec.hide()
        self.inner_rec.hide()
        self.canvas.itemconfigure(self.entry_window, state='hidden')

    def show(self):
        self.outer_rec.show()
        self.inner_rec.show()
        self.canvas.itemconfigure(self.entry_window, state='normal')

    def error(self):
        self.entry.config({ "fg": Color.red, "selectforeground": Color.red, "insertbackground": Color.red })

    def normal(self):
        self.entry.config({ "fg": self.color, "selectforeground": self.color, "insertbackground": self.color })

    def disable(self):
        self.entry.config({ "state": "disabled" })
    
    def enable(self):
        self.entry.config({ "state": "normal" })

    def set_text(self, text):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(text))

    def get_value(self):
        return self.entry.get()
    
    def validate(self, value):
        """
        Parameters
            value (str) : Entry's value 
            limit (int) : Limit of entry's value
        
        Return
            Error code (int) : Error code where
                0 = Normal
                1 = Error number exceed limit value
        """
        valid_character = "0123456789"

        value = str(value)

        # Remove blank space
        value = value.replace(" ", "")
        
        if value != "":
            if int(value) > 600:
                return 1

        return 0