import tkinter as tk
import platform
import time
# from keyboard import Keyboard

from components.color import Color
from components.grid import Grid
from components.tray import Tray
from components.target import Target
from components.navigator import Navigator
from components.button import PressButton, RadioButton, ToggleButton, StatusButton
from components.shape import RoundRectangle, Line
from components.text import TextBox, MessageBox, Error
from components.photo import Photo
from components.entry import Entry, OrderEntry
from BaseSystem.code.protocol import Protocol_Y, Protocol_X

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Title
        self.title('Base System')
        # Mode
        self.mode = "Graphic"
        # self.mode = "Protocol"
        # Define os
        self.os = platform.platform()[0].upper()
        # Window Dimension
        window_width = 740
        window_height = 780
        # Find Window Center
        window_center_x = int(self.winfo_screenwidth()/2 - window_width / 2)
        window_center_y = 0
        # Set Window Properties
        self.geometry(f'{window_width}x{window_height}+{window_center_x}+{window_center_y}')
        self.resizable(False, False)
        self.configure(bg=Color.darkgray)
        # create component
        self.create_components(self.os)
        # Counting Time
        self.time_ms_y = 0
        self.time_ms_x = 0
        # Prepare Protocol
        self.protocol_y = Protocol_Y()
        self.protocol_x = Protocol_X()
        self.connection = True
        self.new_connection = True
        # # Keyboard Control for Developer
        # if self.mode == "Graphic":
        #     self.keyboard = Keyboard(self)
        #     self.keyboard.key_bind(self)
    
    def task(self):
        # Handle Buttons
        self.handle_toggle_vacuum()
        self.handle_radio_operation()

        # if self.mode == "Graphic":
        #     # Handle graphic mode only
        #     self.handle_graphic()

        if self.mode == "Protocol":
            # Handle y-axis protocol
            self.start_time = time.time()
            self.handle_protocol_y()
            # Handle x-axis protocol
            self.handle_protocol_x()

        # Validate Entry Value
        # self.validate_entry()

        # Loop every 10 ms
        self.after(10, self.task)
        self.time_ms_y += 10
        self.time_ms_x += 10  
    
    def create_components(self, os):
        """
        This function creates each UI components
        """
        # Define font size of each os
        if self.os == "M": # Mac
            font_size_title = 14
            font_size_subtitle = 11
            font_size_detail = 9
            font_size_grid = 9
            font_size_sub_grid = 8
            font_size_unit_grid = 6
            font_size_button_small = 12
            font_size_button_home = 15
            font_size_button_run = 22
        elif self.os == "W": # Windows
            font_size_title = 14
            font_size_subtitle = 11
            font_size_detail = 9
            font_size_grid = 9
            font_size_sub_grid = 8
            font_size_unit_grid = 6
            font_size_button_small = 9
            font_size_button_home = 12
            font_size_button_run = 17
            font_size_message_error = 7
        
        # field of table (background)
        self.canvas_field = tk.Canvas(master=self, width=740, height=780, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_field.pack(side="top")
        self.background_field_table = RoundRectangle(canvas=self.canvas_field, x=40, y=30, w=320, h=720, r=10, color=Color.whitegray)
        self.background_field_detail = RoundRectangle(canvas=self.canvas_field, x=380, y=110, w=320, h=640, r=10, color=Color.whitegray)

        # --------------------------------- Group of Grid ---------------------------------
        self.grid = Grid(canvas=self.canvas_field, offset_x=90, offset_y=85, row=63, column=22, color_grid=Color.lightgray , color_highlight=Color.gray)
        self.text_negative_x = TextBox(canvas=self.canvas_field, x=65, y=695, text="-x", font_name="Inter-Bold", font_size=font_size_grid, color=Color.darkgray, anchor="center")
        self.text_unit_negative_x = TextBox(canvas=self.canvas_field, x=65, y=712.5, text="(mm)", font_name="Inter-Regular", font_size=font_size_sub_grid, color=Color.darkgray, anchor="center")
        self.text_positive_x = TextBox(canvas=self.canvas_field, x=335, y=695, text="+x", font_name="Inter-Bold", font_size=font_size_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_x = TextBox(canvas=self.canvas_field, x=335, y=712.5, text="(mm)", font_name="Inter-Regular", font_size=font_size_sub_grid, color=Color.darkgray, anchor="center")
        self.text_positive_z = TextBox(canvas=self.canvas_field, x=200, y=55, text="+z", font_name="Inter-Bold", font_size=font_size_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z = TextBox(canvas=self.canvas_field, x=200, y=72.5, text="(mm)", font_name="Inter-Regular", font_size=font_size_sub_grid, color=Color.darkgray, anchor="center")
    
        self.text_unit_origin = TextBox(canvas=self.canvas_field, x=200, y=725, text="(0,0)", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_x_100 = TextBox(canvas=self.canvas_field, x=300, y=725, text="100", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_negative_x_200 = TextBox(canvas=self.canvas_field, x=100, y=725, text="-100", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z_100 = TextBox(canvas=self.canvas_field, x=210, y=610, text="100", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z_200 = TextBox(canvas=self.canvas_field, x=210, y=510, text="200", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z_300 = TextBox(canvas=self.canvas_field, x=210, y=410, text="300", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z_400 = TextBox(canvas=self.canvas_field, x=210, y=310, text="400", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z_500 = TextBox(canvas=self.canvas_field, x=210, y=210, text="500", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")
        self.text_unit_positive_z_600 = TextBox(canvas=self.canvas_field, x=210, y=110, text="600", font_name="Inter-Regular", font_size=font_size_unit_grid, color=Color.darkgray, anchor="center")

        # ------------------------- Group of all detail and button- ------------------------
        # ------------------------------------- logo ---------------------------------------
        self.text_title = TextBox(canvas=self.canvas_field, x=573, y=55, text="ROBOTICS STUDIO III", font_name="Inter-Bold", font_size=font_size_title, color=Color.whitegray, anchor="center")
        self.text_subtitle = TextBox(canvas=self.canvas_field, x=572, y=85, text="BASE SYSTEM", font_name="Inter-Bold", font_size=font_size_title, color=Color.whitegray, anchor="center")
        self.photo_logo = Photo(canvas=self.canvas_field, file_name="../img/logo.png", x=433, y=70, size_x=52, size_y=52)

        # ---------------------------------- Group detail ----------------------------------
        self.text_detail = TextBox(canvas=self.canvas_field, x=540, y=140, text="Detail", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.text_x_pos = TextBox(canvas=self.canvas_field, x=410, y=165, text="x-Axis Position", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_pos = TextBox(canvas=self.canvas_field, x=410, y=190, text="z-Axis Position", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_spd = TextBox(canvas=self.canvas_field, x=410, y=215, text="z-Axis Speed", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_acc = TextBox(canvas=self.canvas_field, x=410, y=240, text="z-Axis Acceleration", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_x_pos_unit = TextBox(canvas=self.canvas_field, x=630, y=165, text="mm", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_pos_unit = TextBox(canvas=self.canvas_field, x=630, y=190, text="mm", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_spd_unit = TextBox(canvas=self.canvas_field, x=630, y=215, text="mm/s", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_acc_unit = TextBox(canvas=self.canvas_field, x=630, y=240, text="mm/s", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_acc_2= TextBox(canvas=self.canvas_field, x=660, y=235, text="2", font_name="Inter-Regular", font_size=5, color=Color.darkgray, anchor="w")
        self.text_x_pos_num = TextBox(canvas=self.canvas_field, x=570, y=165,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_y_pos_num = TextBox(canvas=self.canvas_field, x=570, y=190,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_y_spd_num = TextBox(canvas=self.canvas_field, x=570, y=215,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_y_acc_num = TextBox(canvas=self.canvas_field, x=570, y=240,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.line_seperate_1 = Line(canvas=self.canvas_field, point_1=(400, 270), point_2=(680, 270), width=1, color=Color.lightgray)

        # ---------------------------------- Group gripper ----------------------------------
        self.vacuum = False
        self.text_gripper = TextBox(canvas=self.canvas_field, x=540, y=300, text="Gripper", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.text_vacuum = TextBox(canvas=self.canvas_field, x=430, y=330, text="Vacuum", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.toggle_vacuum   = ToggleButton(canvas=self.canvas_field, x=395, y=350, w=40, h=20, on_active_color=Color.blue, on_inactive_color=Color.lightblue, on_text="ON", off_active_color=Color.gray, off_inactive_color=Color.lightgray, off_text="OFF", font_name="Inter-Regular", text_size=font_size_button_small, on_default=False)
        
        self.line_gripper = Line(canvas=self.canvas_field, point_1=(480, 325), point_2=(480, 380), width=1, color=Color.lightgray)

        self.gripping = False
        self.text_movement = TextBox(canvas=self.canvas_field, x=590, y=330, text="Movement", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.status_forward = StatusButton(canvas=self.canvas_field, x=500, y=350, w=20, h=20, on_active_color=Color.blue, off_active_color=Color.gray, on_default=False)
        self.status_backward = StatusButton(canvas=self.canvas_field, x=590, y=350, w=20, h=20, on_active_color=Color.blue, off_active_color=Color.gray, on_default=False)
        self.text_forward = TextBox(canvas=self.canvas_field, x=530, y=357.5, text="Forward", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_backward = TextBox(canvas=self.canvas_field, x=620, y=357.5, text="Backword", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.line_seperate_2 = Line(canvas=self.canvas_field, point_1=(400, 387.5), point_2=(680, 387.5), width=1, color=Color.lightgray)

        # ---------------------------------- Group operation ----------------------------------
        self.operation_mode = "Jog"
        self.text_operation = TextBox(canvas=self.canvas_field, x=540, y=412.5, text="Operation", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.line_seperate_2 = Line(canvas=self.canvas_field, point_1=(400, 569.5), point_2=(680, 569.5), width=1, color=Color.lightgray)

            # ------------------------- Jog Mode -------------------------
        self.jogging = False
        self.radio_jog  = RadioButton(canvas=self.canvas_field, x=440, y=437.5, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Jog Mode  ", font_name="Inter-Regular", text_size=font_size_button_small, on_default=True)
        self.text_pick = TextBox(canvas=self.canvas_field, x=410, y=486, text="Pick", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_place = TextBox(canvas=self.canvas_field, x=410, y=524.5, text="Place", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="w")

        self.line_pick_place_1 = Line(canvas=self.canvas_field, point_1=(470, 500), point_2=(470, 509.5), width=1, color=Color.lightgray)
        self.line_pick_place_2 = Line(canvas=self.canvas_field, point_1=(515, 500), point_2=(515, 509.5), width=1, color=Color.lightgray)
        self.line_pick_place_3 = Line(canvas=self.canvas_field, point_1=(560, 500), point_2=(560, 509.5), width=1, color=Color.lightgray)
        self.line_pick_place_4 = Line(canvas=self.canvas_field, point_1=(605, 500), point_2=(605, 509.5), width=1, color=Color.lightgray)
        self.line_pick_place_5 = Line(canvas=self.canvas_field, point_1=(650, 500), point_2=(650, 509.5), width=1, color=Color.lightgray)

        self.entry_pick_1 = OrderEntry(master=self, canvas=self.canvas_field, x=455, y=471, w=30, h=30, color=Color.gray)
        self.entry_pick_2 = OrderEntry(master=self, canvas=self.canvas_field, x=500, y=471, w=30, h=30, color=Color.gray)
        self.entry_pick_3 = OrderEntry(master=self, canvas=self.canvas_field, x=545, y=471, w=30, h=30, color=Color.gray)
        self.entry_pick_4 = OrderEntry(master=self, canvas=self.canvas_field, x=590, y=471, w=30, h=30, color=Color.gray)
        self.entry_pick_5 = OrderEntry(master=self, canvas=self.canvas_field, x=635, y=471, w=30, h=30, color=Color.gray)

        self.entry_place_1 = OrderEntry(master=self, canvas=self.canvas_field, x=455, y=509.5, w=30, h=30, color=Color.gray)
        self.entry_place_2 = OrderEntry(master=self, canvas=self.canvas_field, x=500, y=509.5, w=30, h=30, color=Color.gray)
        self.entry_place_3 = OrderEntry(master=self, canvas=self.canvas_field, x=545, y=509.5, w=30, h=30, color=Color.gray)
        self.entry_place_4 = OrderEntry(master=self, canvas=self.canvas_field, x=590, y=509.5, w=30, h=30, color=Color.gray)
        self.entry_place_5 = OrderEntry(master=self, canvas=self.canvas_field, x=635, y=509.5, w=30, h=30, color=Color.gray)

            # ------------------------- Point Mode -------------------------
        self.radio_point = RadioButton(canvas=self.canvas_field, x=550, y=437.5, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode", font_name="Inter-Regular", text_size=font_size_button_small, on_default=False)
        self.text_z_point = TextBox(canvas=self.canvas_field, x=540, y=490, text="z-axis position", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.text_z_entry = Entry(master=self, canvas=self.canvas_field, x=480, y=507.5, w=100, h=30, color=Color.blue)
        self.text_z_point_mm = TextBox(canvas=self.canvas_field, x=600, y=522.5, text="mm", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.text_z_point.hide()
        self.text_z_entry.hide()
        self.text_z_point_mm.hide()

        # ---------------------------------- Group movement ----------------------------------
        self.text_movement = TextBox(canvas=self.canvas_field, x=540, y=599.5, text="Movement", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.press_home = PressButton(canvas=self.canvas_field, x=465, y=625, w=150, h=30, r=15, active_color=Color.gray, inactive_color=Color.lightgray, text="Home", font_name="Inter-SemiBold", text_size=font_size_button_home, active_default=True)
        self.press_run  = PressButton(canvas=self.canvas_field, x=465, y=675, w=150, h=44, r=22, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", font_name="Inter-SemiBold", text_size=font_size_button_run, active_default=False)
        self.running = False
        self.homing = False

        # ---------------------------------- Error ----------------------------------
        self.message_error = MessageBox(canvas=self.canvas_field, x=380, y=460, width_field=320, text="Input x for Point Mode must be one number (integer)", color=Color.red, align="Center", font_name="Inter-SemiBold", size=font_size_message_error)
        self.message_error.hide()

        self.canvas_field.bind("<ButtonRelease-1>", self.mouse_position)
        self.grid.canvas.bind("<Button-1>", lambda event: self.grid.on_click(event, self.operation_mode))
    
    def handle_radio_operation(self):
        """
        This function handles when user press radio button (choose operation mode)
        """
        # Click Point Mode
        if self.operation_mode == "Jog" and self.radio_point.on:
            self.radio_jog.turn_off()
            self.operation_mode = "Point"
            self.text_pick.hide()
            self.text_place.hide()

            self.line_pick_place_1.hide()
            self.line_pick_place_2.hide()
            self.line_pick_place_3.hide()
            self.line_pick_place_4.hide()
            self.line_pick_place_5.hide()

            self.entry_pick_1.hide()
            self.entry_pick_2.hide()
            self.entry_pick_3.hide()
            self.entry_pick_4.hide()
            self.entry_pick_5.hide()

            self.entry_place_1.hide()
            self.entry_place_2.hide()
            self.entry_place_3.hide()
            self.entry_place_4.hide()
            self.entry_place_5.hide()

            self.text_z_point.show()
            self.text_z_entry.show()
            self.text_z_point_mm.show()
        # Click Jog Mode
        elif self.operation_mode == "Point" and self.radio_jog.on:
            self.radio_point.turn_off()
            self.operation_mode = "Jog"
            self.text_pick.show()
            self.text_place.show()

            self.line_pick_place_1.show()
            self.line_pick_place_2.show()
            self.line_pick_place_3.show()
            self.line_pick_place_4.show()
            self.line_pick_place_5.show()

            self.entry_pick_1.show()
            self.entry_pick_2.show()
            self.entry_pick_3.show()
            self.entry_pick_4.show()
            self.entry_pick_5.show()

            self.entry_place_1.show()
            self.entry_place_2.show()
            self.entry_place_3.show()
            self.entry_place_4.show()
            self.entry_place_5.show()

            self.text_z_point.hide()
            self.text_z_entry.hide()
            self.text_z_point_mm.hide()
    
    def turn_on_vacuum(self):
        """
        This function turns on vacuum with protocol, turn on vacuum toggle, show vacuum on UI's navigator
        """
        if self.mode == "Graphic":
            self.protocol_y.laser_on = "1"
        elif self.mode == "Protocol":
            self.protocol_y.write_end_effector_status("Vacuum On")
        self.toggle_vacuum.turn_on()
    
    def turn_off_vacuum(self):
        """
        This function turns off vacuum with protocol, turn off vacuum toggle, hide vacuum on UI's navigator
        """
        if self.mode == "Graphic":
            self.protocol_y.laser_on = "0"
        elif self.mode == "Protocol":
            self.protocol_y.write_end_effector_status("Vacuum Off")
        self.toggle_vacuum.turn_off()
    
    def handle_toggle_vacuum(self):
        """
        This function handles when user press vacuum toggle
        """
        if self.toggle_vacuum.pressed:
            # Turn vacuum On
            if not self.toggle_vacuum.on:
                self.turn_on_vacuum()
            # Turn vacuum Off
            else:
                self.turn_off_vacuum()
            self.toggle_vacuum.pressed = False
    
    def mouse_position(self, event):
        """
        This function is called when user click on the grid during point mode,
        then move the target and change entry text
        """
        if self.operation_mode == "Point" and self.connection and (self.protocol_y.usb_connect or self.mode == "Graphic"):
            if not self.running and not self.homing and not self.jogging and not self.gripping and not self.vacuum:
                self.point_target_z = self.grid.on_click(event, self.operation_mode)
                # Set text in entry
                self.text_z_entry.set_text(self.point_target_z)


if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()