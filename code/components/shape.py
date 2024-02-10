class Oval():
    """
    Oval Class
    """
    def __init__(self, canvas, x, y, d, fill_color, outline_color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.d = d
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.oval = self.canvas.create_oval(x, y, x+d, y+d, fill=self.fill_color, outline=self.outline_color, width=2) 

    def hide(self):
        self.canvas.itemconfigure(self.oval, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.oval, state='normal')
    
    def activate(self, active_color):
        self.canvas.itemconfigure(self.oval, fill=active_color)

    def deactivate(self, inactive_color):
        self.canvas.itemconfigure(self.oval, fill=inactive_color)

    def move_to(self, x, y):
        self.canvas.move(self.oval, x-self.x, y-self.y)
        self.x = x
        self.y = y


class Rectangle():
    def __init__(self, canvas, x, y, w, h, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.rect  = self.canvas.create_rectangle(x, y, x+w, y+h, fill=self.color, outline='')

    def hide(self):
        self.canvas.itemconfigure(self.rect, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.rect, state='normal')

    def activate(self, active_color):
        self.canvas.itemconfigure(self.rect, fill=active_color)

    def deactivate(self, inactive_color):
        self.canvas.itemconfigure(self.rect, fill=inactive_color)

    def move_to(self, x, y):
        self.canvas.move(self.rect, x-self.x, y-self.y)
        self.x = x
        self.y = y

    def resize(self, w, h):
        self.canvas.coords(self.rect, self.x, self.y, self.x+w, self.y+h)
        self.w = w
        self.h = h
    

class RoundRectangle():
    """
    Round Rectangle Class
    """
    def __init__(self, canvas, x, y, w, h, r, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.color = color
        self.oval_1 = Oval(self.canvas, x,       y,       2*r, fill_color=self.color, outline_color="")
        self.oval_2 = Oval(self.canvas, x+w-2*r, y,       2*r, fill_color=self.color, outline_color="")
        self.oval_3 = Oval(self.canvas, x,       y+h-2*r, 2*r, fill_color=self.color, outline_color="")
        self.oval_4 = Oval(self.canvas, x+w-2*r, y+h-2*r, 2*r, fill_color=self.color, outline_color="")
        self.rec_1  = Rectangle(self.canvas, x+r, y,   w-2*r, h,   self.color)
        self.rec_2  = Rectangle(self.canvas, x,   y+r, w,   h-2*r, self.color)

    def hide(self):
        self.oval_1.hide()
        self.oval_2.hide()
        self.oval_3.hide()
        self.oval_4.hide()
        self.rec_1.hide()
        self.rec_2.hide()

    def show(self):
        self.oval_1.show()
        self.oval_2.show()
        self.oval_3.show()
        self.oval_4.show()
        self.rec_1.show()
        self.rec_2.show()

    def activate(self, active_color):
        self.oval_1.activate(active_color)
        self.oval_2.activate(active_color)
        self.oval_3.activate(active_color)
        self.oval_4.activate(active_color)
        self.rec_1.activate(active_color)
        self.rec_2.activate(active_color)

    def deactivate(self, inactive_color):
        self.oval_1.deactivate(inactive_color)
        self.oval_2.deactivate(inactive_color)
        self.oval_3.deactivate(inactive_color)
        self.oval_4.deactivate(inactive_color)
        self.rec_1.deactivate(inactive_color)
        self.rec_2.deactivate(inactive_color)

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.oval_1.move_to(x, y)
        self.oval_2.move_to(x+self.w-2*self.r, y)
        self.oval_3.move_to(x, y+self.h-2*self.r)
        self.oval_4.move_to(x+self.w-2*self.r, y+self.h-2*self.r)
        self.rec_1.move_to(x+self.r, y)
        self.rec_2.move_to(x, y+self.r)

    def resize(self, w, h):
        self.rec_1.resize(w-2*self.r, h)
        self.rec_2.resize(w, h-2*self.r)
        self.oval_2.move_to(self.x+w-2*self.r, self.y)
        self.oval_3.move_to(self.x,            self.y+h-2*self.r)
        self.oval_4.move_to(self.x+w-2*self.r, self.y+h-2*self.r)
        self.w = w
        self.h = h


class Polygon():
    """
    Polygon Class
    """
    def __init__(self, canvas, points, color):
        self.canvas = canvas
        self.points = points
        self.color = color
        self.polygon = self.canvas.create_polygon(*points, fill=self.color, outline="")

    def move(self, x_shift, y_shift):
        self.canvas.move(self.polygon, x_shift, y_shift)

    def clear(self):
        self.canvas.delete(self.polygon)

    def hide(self):
        self.canvas.itemconfigure(self.polygon, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.polygon, state='normal')

    def recreate(self, points):
        polygon_points = []
        for i in range(len(points)):
            polygon_points.append(points[i][0])
            polygon_points.append(points[i][1])
        self.canvas.coords(self.polygon, *polygon_points)


class FreeOval():
    """
    Free Oval Class
    """
    def __init__(self, canvas, point_1, point_2, fill_color, outline_color=""):
        self.canvas = canvas
        self.point_1 = point_1
        self.point_2 = point_2
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.free_oval = self.canvas.create_oval(self.point_1, self.point_2, fill=self.fill_color, outline=self.outline_color, width=2)

    def move(self, x_shift, y_shift):
        self.canvas.move(self.free_oval, x_shift, y_shift)

    def clear(self):
        self.canvas.delete(self.free_oval)

    def hide(self):
        self.canvas.itemconfigure(self.free_oval, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.free_oval, state='normal')


class Line():
    """
    Line Class
    """
    def __init__(self, canvas, point_1, point_2, width, color):
        self.canvas = canvas
        self.point_1 = point_1
        self.point_2 = point_2
        self.width = width
        self.color = color
        self.line = self.canvas.create_line(point_1, point_2, width=self.width, fill=self.color)

    def hide(self):
        self.canvas.itemconfigure(self.line, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.line, state='normal')

    def move(self, x_shift, y_shift):
        self.canvas.move(self.line, x_shift, y_shift)