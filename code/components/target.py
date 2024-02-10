from components.color import Color
from components.shape import FreeOval, Line

class Target():
    """
    Target class
    """
    def __init__(self, canvas, grid, grid_x, grid_y):
        self.canvas = canvas 
        self.grid = grid
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pixel_x = 0
        self.pixel_y = 0
        target_points = self.map_points()
        self.target_inner = FreeOval(canvas=self.canvas, point_1=target_points["inner_oval"][0], point_2=target_points["inner_oval"][1], fill_color=Color.blue)
        self.target_outer = FreeOval(canvas=self.canvas, point_1=target_points["outer_oval"][0], point_2=target_points["outer_oval"][1], fill_color='', outline_color=Color.blue)
        self.target_ticks = []
        for i in range(4):
            self.target_ticks.append(Line(canvas=self.canvas, point_1=target_points["tick"][i][0], point_2=target_points["tick"][i][1], width=2, color=Color.blue))

    def hide(self):
        self.target_inner.hide()
        self.target_outer.hide()
        for i in range(4):
            self.target_ticks[i].hide()

    def show(self):
        self.target_inner.show()
        self.target_outer.show()
        for i in range(4):
            self.target_ticks[i].show()

    def move_to(self, grid_x, grid_y):
        old_points = self.map_points()["center"]
        self.grid_x = grid_x
        self.grid_y = grid_y
        new_points = self.map_points()["center"]
        x_shift = new_points[0] - old_points[0]
        y_shift = new_points[1] - old_points[1]
        self.target_inner.move(x_shift, y_shift)
        self.target_outer.move(x_shift, y_shift)
        for i in range(4):
            self.target_ticks[i].move(x_shift, y_shift)
    
    def map_points(self):
        pixel_x, pixel_y = self.grid.map_3D_to_2D(self.grid_x, self.grid_y, 0)
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        target_points = {
            "center" : (pixel_x, pixel_y),
            "inner_oval" : (
                (pixel_x - 4, pixel_y + 2),
                (pixel_x + 4, pixel_y - 2)
            ),
            "outer_oval" : (
                (pixel_x - 10, pixel_y + 5),
                (pixel_x + 10, pixel_y - 5)
            ),
            "tick" : [
                ((pixel_x+12, pixel_y+6), (pixel_x+8, pixel_y+4)),
                ((pixel_x+12, pixel_y-6), (pixel_x+8, pixel_y-4)),
                ((pixel_x-12, pixel_y-6), (pixel_x-8, pixel_y-4)),
                ((pixel_x-12, pixel_y+6), (pixel_x-8, pixel_y+4)),  
            ]
        }
        return target_points