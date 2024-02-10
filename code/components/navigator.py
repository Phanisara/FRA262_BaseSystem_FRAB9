from components.color import Color
from components.shape import Polygon, Line, FreeOval

class Navigator():
    """
    Navigator class
    """
    def __init__(self, canvas, grid, grid_x, grid_y, grid_z, pick_tray, place_tray):
        self.canvas = canvas
        self.grid = grid
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_z = grid_z
        self.pixel_x = 0
        self.pixel_y = 0
        self.pick_tray = pick_tray
        self.place_tray = place_tray
        self.over_tray = False

        navigator_points = self.map_points()
        self.navigator_laser = Line(canvas=self.canvas, point_1=navigator_points["navigator_laser"][0], point_2=navigator_points["navigator_laser"][1], width=2, color=Color.red)
        self.navigator_top   = Polygon(canvas=self.canvas, points=navigator_points["navigator_top"], color="#FFD18C")
        self.navigator_left  = Polygon(canvas=self.canvas, points=navigator_points["navigator_left"], color="#FFB545")
        self.navigator_right = Polygon(canvas=self.canvas, points=navigator_points["navigator_right"], color="#EAA031")
        self.navigator_oval  = FreeOval(canvas=self.canvas, point_1=navigator_points["navigator_oval"][0], point_2=navigator_points["navigator_oval"][1], fill_color=Color.red)
        self.navigator_laser.hide()

    def map_points(self):
        pixel_x, pixel_y = self.grid.map_3D_to_2D(self.grid_x, self.grid_y, self.grid_z)
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

        navigator_points = {
            "navigator_tip" : (pixel_x, pixel_y),
            "navigator_top" : (
                (pixel_x,      pixel_y - 16),
                (pixel_x - 16, pixel_y - 24),
                (pixel_x,      pixel_y - 32),
                (pixel_x + 16, pixel_y - 24),
            ),
            "navigator_left" : (
                (pixel_x,      pixel_y),
                (pixel_x - 16, pixel_y - 24),
                (pixel_x,      pixel_y - 16),
            ),
            "navigator_right" : (
                (pixel_x,      pixel_y),
                (pixel_x + 16, pixel_y - 24),
                (pixel_x,      pixel_y - 16),
            ),
            "navigator_laser" : (
                (pixel_x, pixel_y-5),
                (pixel_x, pixel_y+self.grid_z*8)
            ),
            "navigator_oval" : (
                (pixel_x-4, pixel_y-2+self.grid_z*8), 
                (pixel_x+4, pixel_y+2+self.grid_z*8)
            )
        }
        return navigator_points
    
    def move_to(self, grid_x, grid_y):
        old_points = self.map_points()["navigator_tip"]
        self.grid_x = grid_x
        self.grid_y = grid_y
        new_points = self.map_points()["navigator_tip"]
        x_shift = new_points[0] - old_points[0]
        y_shift = new_points[1] - old_points[1]
        self.navigator_top.move(x_shift, y_shift)
        self.navigator_left.move(x_shift, y_shift)
        self.navigator_right.move(x_shift, y_shift)
        self.navigator_laser.move(x_shift, y_shift)
        self.navigator_oval.move(x_shift, y_shift)
        self.laser_tray()

    def laser_tray(self):
        overlap_objects = self.canvas.find_overlapping(self.pixel_x-4, self.pixel_y-2+self.grid_z*8, self.pixel_x+4, self.pixel_y+2+self.grid_z*8)
        if self.pick_tray.tray_bottom.polygon in overlap_objects or self.place_tray.tray_bottom.polygon in overlap_objects:
            if not self.over_tray:
                self.navigator_oval.move(0, -4)
                self.navigator_laser.move(0, -4)
                self.over_tray = True
        else:
            if self.over_tray:
                self.navigator_oval.move(0, 4)
                self.navigator_laser.move(0, 4)
                self.over_tray = False