class Grid():
    """
    Grid class
    root_canvas (canvas) : root canvas
    offset_x (int) : top left origin x
    offset_y (int) : top left origin y
    row (int)    : number of rows
    column (int) : number of columns
    color (str)  : color code 
    """
    def __init__(self, canvas, offset_x, offset_y, row, column, color_grid, color_highlight):
        self.canvas = canvas
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.row = row
        self.column = column
        self.color_grid = color_grid
        self.color_highlight = color_highlight
        self.z_value = None  # Initialize z value variable
        self.previous_dot = None
        self.create_grid()

    def create_grid(self):
        x = self.offset_x
        y = self.offset_y

        # Create horizontal grid lines
        for r in range(self.row + 1):
            self.canvas.create_line((x, y + r * 10), (x + self.column * 10, y + r * 10), width=1, fill=self.color_grid)

        # Create vertical grid lines
        for c in range(self.column + 1):
            self.canvas.create_line((x + c * 10, y), (x + c * 10, y + self.row * 10), width=1, fill=self.color_grid)

        # Highlight the line in row 2 from bottom
        self.canvas.create_line((x, y + (self.row - 1) * 10), (x + self.column * 10, y + (self.row - 1) * 10), width=2, fill=self.color_highlight)

        # Highlight the vertical line at column 11
        self.canvas.create_line((x + 11 * 10, y), (x + 11 * 10, y + self.row * 10), width=2, fill=self.color_highlight)
    
        # Draw short lines along the z-axis
        for i in range(90, self.row * 10, 100):
            self.canvas.create_line((x + 11 * 10 - 5, y + i - 70), (x + 11 * 10 + 5, y + i - 70), width=1.5, fill=self.color_highlight)

        # Draw short lines along the x-axis
        for j in range(0, self.column * 10, 100):
            self.canvas.create_line((x + j + 10, y + (self.row - 1) * 10 - 5), (x + j + 10, y + (self.row - 1) * 10 + 5), width=1.5, fill=self.color_highlight)
    
    def on_click(self, event, operation_mode):
        if operation_mode == 'Point':
            x = event.x
            y = event.y

            # Check if the click event occurs within the grid boundaries
            if (self.offset_x + 10) <= x < (self.offset_x + self.column * 10) and (self.offset_y + 10) <= y <= (self.offset_y + self.row * 10 - 10):
                x_intersection = (x // 10) * 10
                y_intersection = ((y // 10) * 10) + 5


                # Clear the previous dot
                if self.previous_dot:
                    self.canvas.delete(self.previous_dot)

                # Draw a red dot at the intersection of grid lines
                dot = self.canvas.create_oval(x_intersection - 2, y_intersection - 2, x_intersection + 2, y_intersection + 2, fill="red", outline = "red")
                self.previous_dot = dot

                # Save the x and y-axis values
                x_value = x_intersection - 200
                z_value = 705 - y_intersection
                self.saved_position = (x_value, z_value)
                print(f"Clicked at grid (x={x_value}, z={z_value})")
                return x_value, z_value
            else:
                return None, None
    
    def show_point(self, position_z, operation_mode):
        if operation_mode == 'Point':
            # Check if the click event occurs within the grid boundaries
            if (self.offset_y + 10) <= 705 - int(position_z) <= (self.offset_y + self.row * 10 - 10):
                position_z = int(position_z)
                # Clear the previous dot
                if self.previous_dot:
                    self.canvas.delete(self.previous_dot)

                # Draw a red dot at the intersection of grid lines
                dot = self.canvas.create_oval(198, 703 - position_z, 202, 707 - position_z, fill="red", outline = "red")
                self.previous_dot = dot

                z_value = 705 + position_z
                print(f"Entry the position (x=0, z={z_value})")
                return z_value
            else:
                return None