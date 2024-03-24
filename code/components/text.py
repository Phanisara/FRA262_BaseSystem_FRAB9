import platform
from components.shape import RoundRectangle, Polygon
from components.color import Color

class TextBox():
    def __init__(self, canvas, x, y, text, font_name, font_size, color, anchor=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.size = font_size
        self.color = color
        self.os = platform.platform()[0].upper()
        font_name_W = font_name.replace("-", " ")
        if self.os == 'M': #Mac
            self.textbox = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=(font_name, self.size))
        elif self.os == 'W': #Windows  
            self.textbox = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=(font_name_W, self.size))
        if anchor != None:
            self.canvas.itemconfigure(self.textbox, anchor=anchor)

    def activate(self, active_text, active_color):
        self.canvas.itemconfigure(self.textbox, text=active_text, fill=active_color)

    def deactivate(self, inactive_text, inactive_color):
        self.canvas.itemconfigure(self.textbox, text=inactive_text, fill=inactive_color)

    def hide(self):
        self.canvas.itemconfigure(self.textbox, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.textbox, state='normal')

    def change_text(self, text, color=None):
        if color:
            self.canvas.itemconfigure(self.textbox, text=text, fill=color)
        else:
            self.canvas.itemconfigure(self.textbox, text=text)
        self.text = text

    def move_to(self, x, y):
        self.canvas.move(self.textbox, x-self.x, y-self.y)
        self.x = x
        self.y = y


class MessageBox():
    def __init__(self, canvas, x, y, width_field, text, color, align, font_name, size):
        self.canvas = canvas
        self.text = text
        self.align = align
        self.size = size
        self.w = int(len(self.text) * 5)
        self.h = 16
        self.x = x
        self.y = y
        self.r = 6
        self.color = color
        self.font_name = font_name
        self.textbox = TextBox(canvas=self.canvas, x=self.x+(width_field/2), y=self.y + (self.h/2), font_name=self.font_name, text=self.text, font_size=self.size, color=Color.red, anchor="center")

    def hide(self):
        self.textbox.hide()

    def show(self):
        self.textbox.show()

    def change_text(self, text):
        self.textbox.change_text(text)
        self.text = text
        self.w = int(len(self.text) * 5)

class Error:
    code_point_1  = "\" Input for Point Mode Exceed The Limit 600 \""