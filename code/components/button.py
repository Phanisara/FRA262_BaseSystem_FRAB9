from components.color import Color
from components.shape import Oval, Rectangle, RoundRectangle
from components.photo import Photo
from components.text import TextBox

class Button():
    """
    Button class
    """
    def create_click_area(self, w, h):
        return Rectangle(self.canvas, self.x, self.y, w, h, color="")
        

class PressButton(Button):
    """
    RectangleButton Class
    """
    def __init__(self, canvas, x, y, w, h, r, active_color, inactive_color, text, text_size, font_name, active_default, image=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.font_name = font_name
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text = text
        self.text_size = text_size
        self.active = active_default
        self.image = image
        self.pressed = False
        self.round_rec = RoundRectangle(self.canvas, x, y, w, h, r, color=self.active_color)
        self.textbox = TextBox(self.canvas, x+w/2, y+h/2, self.text, self.font_name, self.text_size, Color.white)
        if self.image != None:
            self.photo_arrow_pick  = Photo(canvas=canvas, file_name="arrow_pick",  x=130, y=124)
            self.photo_arrow_place = Photo(canvas=canvas, file_name="arrow_place", x=130, y=124)
            self.photo_arrow_place.hide()
        self.click_area = self.create_click_area(self.w, self.h)
        self.canvas.tag_bind(self.click_area.rect, "<ButtonRelease-1>", self.clicked)
        if self.active == False:
            self.deactivate()

    def hide(self):
        self.round_rec.hide()
        self.textbox.hide()
        self.click_area.hide()

    def show(self):
        self.round_rec.show()
        self.textbox.show()
        self.click_area.show()

    def activate(self):
        self.active = True
        self.round_rec.activate(self.active_color)
    
    def deactivate(self):
        self.active = False
        self.round_rec.deactivate(self.inactive_color)

    def clicked(self, event):
        if self.active:
            self.pressed = True

    def change_text(self, text):
        self.textbox.change_text(text)


class RadioButton(Button):
    """
    RadioButton class
    """
    def __init__(self, canvas, x, y, r, active_color, inactive_color, text, text_size, font_name, on_default):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.font_name = font_name
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text = text
        self.text_size = text_size
        self.active = True
        self.on = on_default
        self.outer_oval = Oval(self.canvas, x, y, r, fill_color="", outline_color=self.active_color)
        self.inner_oval = Oval(self.canvas, x+4, y+4, r-8, fill_color=self.active_color, outline_color="")
        self.textbox = TextBox(self.canvas, x+55, y+r/2, self.text, self.font_name, self.text_size, self.active_color)
        self.click_area = self.create_click_area(85, r)
        self.canvas.tag_bind(self.click_area.rect, "<ButtonRelease-1>", self.clicked)
        if self.on == False:
            self.turn_off()

    def turn_on(self):
        self.on = True
        self.canvas.itemconfigure(self.outer_oval.oval, outline=self.active_color)
        self.inner_oval.show()
        self.textbox.activate(self.text, self.active_color)
    
    def turn_off(self):
        self.on = False
        self.canvas.itemconfigure(self.outer_oval.oval, outline=self.inactive_color)
        self.inner_oval.hide()
        self.textbox.deactivate(self.text, self.inactive_color)

    def clicked(self, event):
        if self.active and not self.on:
            self.turn_on()

    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False


class ToggleButton(Button):
    """
    ToggleButton class
    """
    def __init__(self, canvas, x, y, w, h, on_active_color, on_inactive_color, on_text, off_active_color, off_inactive_color, off_text, text_size, font_name, on_default):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font_name = font_name
        self.on_active_color = on_active_color
        self.on_inactive_color = on_inactive_color
        self.on_text  = on_text
        self.off_active_color = off_active_color
        self.off_inactive_color = off_inactive_color
        self.off_text  = off_text
        self.text_size = text_size
        self.on = on_default
        self.active = True
        self.pressed = False
        self.round_rec = RoundRectangle(self.canvas, x, y, w, h, h/2, self.on_active_color)
        self.oval      = Oval(self.canvas, x+w-h+3, y+3, h-6, fill_color=Color.white, outline_color="")
        self.textbox = TextBox(self.canvas, x+50, y+h/2, self.on_text, self.font_name, self.text_size, self.on_active_color, anchor="w")
        self.click_area = self.create_click_area(w, h)
        self.canvas.tag_bind(self.click_area.rect, "<ButtonRelease-1>", self.clicked)
        if not self.on:
            self.turn_off()

    def turn_on(self):
        self.on = True
        self.round_rec.activate(self.on_active_color)
        self.canvas.move(self.oval.oval, self.w-self.h, 0)
        self.textbox.activate(self.on_text, self.on_active_color)
    
    def turn_off(self):
        self.on = False
        self.round_rec.deactivate(self.off_active_color)
        self.canvas.move(self.oval.oval, self.h-self.w, 0)
        self.textbox.deactivate(self.off_text, self.off_active_color)

    def clicked(self, event):
        if self.active:
            self.pressed = True

    def activate(self):
        if self.on:
            self.round_rec.activate(self.on_active_color)
        else:
            self.round_rec.activate(self.off_active_color)
        self.active = True
    
    def deactivate(self):
        if self.on:
            self.round_rec.deactivate(self.on_inactive_color)
        else:
            self.round_rec.deactivate(self.off_inactive_color)
        self.active = False

class StatusButton(Button):
    """
    StatusButton class
    """
    def __init__(self, canvas, x, y, w, h, on_active_color, off_active_color, on_default):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.on_active_color = on_active_color
        self.off_active_color = off_active_color
        self.on = on_default
        self.oval = self.canvas.create_oval(x, y, x + h, y + h, fill=self.off_active_color, outline="")
        if not self.on:
            self.turn_off()
        
    def turn_on(self):
        self.on = True
        self.canvas.itemconfig(self.oval, fill=self.on_active_color)
    
    def turn_off(self):
        self.on = False
        self.canvas.itemconfig(self.oval, fill=self.off_active_color)