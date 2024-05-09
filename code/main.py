import tkinter as tk
import platform
import time

from components.color import Color
from components.grid import Grid
from components.target import Target
from components.navigator import Navigator
from components.button import PressButton, RadioButton, ToggleButton, StatusButton
from components.shape import RoundRectangle, Line
from components.text import TextBox, MessageBox, Error
from components.photo import Photo
from components.entry import Entry, OrderEntry
from protocol import Protocol_Z

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Title
        self.title('Base System')
        # Mode
        # self.mode = "Graphic"
        self.mode = "Protocol"
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
        self.protocol_z = Protocol_Z()
        # self.protocol_x = Protocol_X()
        self.connection = True
        self.new_connection = True
        # # Keyboard Control for Developer
        # if self.mode == "Graphic":
        #     self.keyboard = Keyboard(self)
        #     self.keyboard.key_bind(self)
    
    def task(self):
        # Handle Buttons
        self.handle_toggle_vacuum()
        self.handle_toggle_movement()
        self.handle_radio_operation()
        self.handle_press_set_shelves()
        self.handle_press_home()
        self.handle_press_run()
        
        # if self.mode == "Graphic":
        #     # Handle graphic mode only
        #     self.handle_graphic()

        if self.mode == "Protocol":
            # Handle z-axis protocol
            self.start_time = time.time()
            self.handle_protocol_z()
            # Handle x-axis protocol
            # self.handle_protocol_x()

        # Validate Entry Value
        self.validate_entry()

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
            font_size_title = 12
            font_size_subtitle = 11
            font_size_detail = 9
            font_size_grid = 9
            font_size_sub_grid = 8
            font_size_unit_grid = 6
            font_size_button_small = 9
            font_size_button_home = 12
            font_size_button_run = 17
            font_size_message_error = 7
        elif self.os == "W": # Windows
            font_size_title = 12
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
        self.background_field_detail = RoundRectangle(canvas=self.canvas_field, x=380, y=70, w=320, h=680, r=10, color=Color.whitegray)

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
        self.text_title = TextBox(canvas=self.canvas_field, x=540, y=45, text="ROBOTICS STUDIO III : BASE SYSTEM", font_name="Inter-Bold", font_size=font_size_title, color=Color.whitegray, anchor="center")

        # ---------------------------------- Group detail ----------------------------------
        self.text_detail = TextBox(canvas=self.canvas_field, x=540, y=100, text="Detail", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.text_x_pos = TextBox(canvas=self.canvas_field, x=410, y=125, text="x-Axis Position", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_pos = TextBox(canvas=self.canvas_field, x=410, y=150, text="z-Axis Position", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_spd = TextBox(canvas=self.canvas_field, x=410, y=175, text="z-Axis Speed", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_acc = TextBox(canvas=self.canvas_field, x=410, y=200, text="z-Axis Acceleration", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_status = TextBox(canvas=self.canvas_field, x=410, y=225, text="z-Axis Status", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_x_pos_unit = TextBox(canvas=self.canvas_field, x=630, y=125, text="mm", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_pos_unit = TextBox(canvas=self.canvas_field, x=630, y=150, text="mm", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_spd_unit = TextBox(canvas=self.canvas_field, x=630, y=175, text="mm/s", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_acc_unit = TextBox(canvas=self.canvas_field, x=630, y=200, text="mm/s", font_name="Inter-Regular", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_z_acc_2= TextBox(canvas=self.canvas_field, x=660, y=195, text="2", font_name="Inter-Regular", font_size=5, color=Color.darkgray, anchor="w")
        self.text_x_pos_num = TextBox(canvas=self.canvas_field, x=570, y=125,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_z_pos_num = TextBox(canvas=self.canvas_field, x=570, y=150,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_z_spd_num = TextBox(canvas=self.canvas_field, x=570, y=175,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_z_acc_num = TextBox(canvas=self.canvas_field, x=570, y=200,  text="0.0", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.text_z_status_value = TextBox(canvas=self.canvas_field, x=570, y=225,  text="Idle", font_name="Inter-Medium", font_size=font_size_detail, color=Color.blue, anchor="w")
        self.line_seperate_1 = Line(canvas=self.canvas_field, point_1=(400, 250), point_2=(680, 250), width=1, color=Color.lightgray)

        # ---------------------------------- Group gripper ----------------------------------
        self.vacuum = False
        self.text_gripper = TextBox(canvas=self.canvas_field, x=540, y=270, text="Gripper", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.text_vacuum = TextBox(canvas=self.canvas_field, x=450, y=295, text="Vacuum", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.toggle_vacuum   = ToggleButton(canvas=self.canvas_field, x=415, y=315, w=40, h=20, on_active_color=Color.blue, on_inactive_color=Color.lightblue, on_text="ON", off_active_color=Color.gray, off_inactive_color=Color.lightgray, off_text="OFF", font_name="Inter-Regular", text_size=font_size_button_small, on_default=False)
        
        self.line_gripper = Line(canvas=self.canvas_field, point_1=(520, 290), point_2=(520, 345), width=1, color=Color.lightgray)

        self.gripping = False
        self.text_movement = TextBox(canvas=self.canvas_field, x=610, y=295, text="Movement", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.toggle_movement   = ToggleButton(canvas=self.canvas_field, x=545, y=315, w=40, h=20, on_active_color=Color.blue, on_inactive_color=Color.lightblue, on_text="FORWARD", off_active_color=Color.gray, off_inactive_color=Color.lightgray, off_text="BACKWARD", font_name="Inter-Regular", text_size=font_size_button_small, on_default=False)
        
        self.text_reed_switch_1 = TextBox(canvas=self.canvas_field, x=450, y=363, text="Reed Switch 1: ", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.text_reed_switch_2 = TextBox(canvas=self.canvas_field, x=590, y=363, text="Reed Switch 2: ", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.status_reed_switch_1 = TextBox(canvas=self.canvas_field, x=500, y=363,  text="OFF", font_name="Inter-Medium", font_size=font_size_detail, color=Color.gray, anchor="w")
        self.status_reed_switch_2 = TextBox(canvas=self.canvas_field, x=640, y=363,  text="OFF", font_name="Inter-Medium", font_size=font_size_detail, color=Color.gray, anchor="w")

        self.line_seperate_2 = Line(canvas=self.canvas_field, point_1=(400, 387.5), point_2=(680, 387.5), width=1, color=Color.lightgray)

        # ---------------------------------- Group operation ----------------------------------
        self.operation_mode = "Jog"
        self.text_operation = TextBox(canvas=self.canvas_field, x=540, y=412.5, text="Operation", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.line_seperate_2 = Line(canvas=self.canvas_field, point_1=(400, 594.5), point_2=(680, 594.5), width=1, color=Color.lightgray)

        # ------------------------- Jog Mode -------------------------
        self.jogging = False
        self.radio_jog  = RadioButton(canvas=self.canvas_field, x=440, y=437.5, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Jog Mode  ", font_name="Inter-Regular", text_size=font_size_button_small, on_default=True)
        self.press_set_shelves = PressButton(canvas=self.canvas_field, x=465, y=467, w=150, h=20, r=10, active_color=Color.gray, inactive_color=Color.lightgray, text="Set shelves", font_name="Inter-SemiBold", text_size=font_size_detail, active_default=True)
        self.text_pick = TextBox(canvas=self.canvas_field, x=410, y=516, text="Pick", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="w")
        self.text_place = TextBox(canvas=self.canvas_field, x=410, y=554.5, text="Place", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="w")
    
        self.line_pick_place_1 = Line(canvas=self.canvas_field, point_1=(470, 530), point_2=(470, 539.5), width=1, color=Color.lightgray)
        self.line_pick_place_2 = Line(canvas=self.canvas_field, point_1=(515, 530), point_2=(515, 539.5), width=1, color=Color.lightgray)
        self.line_pick_place_3 = Line(canvas=self.canvas_field, point_1=(560, 530), point_2=(560, 539.5), width=1, color=Color.lightgray)
        self.line_pick_place_4 = Line(canvas=self.canvas_field, point_1=(605, 530), point_2=(605, 539.5), width=1, color=Color.lightgray)
        self.line_pick_place_5 = Line(canvas=self.canvas_field, point_1=(650, 530), point_2=(650, 539.5), width=1, color=Color.lightgray)

        self.entry_pick_1 = OrderEntry(master=self, canvas=self.canvas_field, x=455, y=501, w=30, h=30, color=Color.gray)
        self.entry_pick_2 = OrderEntry(master=self, canvas=self.canvas_field, x=500, y=501, w=30, h=30, color=Color.gray)
        self.entry_pick_3 = OrderEntry(master=self, canvas=self.canvas_field, x=545, y=501, w=30, h=30, color=Color.gray)
        self.entry_pick_4 = OrderEntry(master=self, canvas=self.canvas_field, x=590, y=501, w=30, h=30, color=Color.gray)
        self.entry_pick_5 = OrderEntry(master=self, canvas=self.canvas_field, x=635, y=501, w=30, h=30, color=Color.gray)

        self.entry_place_1 = OrderEntry(master=self, canvas=self.canvas_field, x=455, y=539.5, w=30, h=30, color=Color.gray)
        self.entry_place_2 = OrderEntry(master=self, canvas=self.canvas_field, x=500, y=539.5, w=30, h=30, color=Color.gray)
        self.entry_place_3 = OrderEntry(master=self, canvas=self.canvas_field, x=545, y=539.5, w=30, h=30, color=Color.gray)
        self.entry_place_4 = OrderEntry(master=self, canvas=self.canvas_field, x=590, y=539.5, w=30, h=30, color=Color.gray)
        self.entry_place_5 = OrderEntry(master=self, canvas=self.canvas_field, x=635, y=539.5, w=30, h=30, color=Color.gray)
    
            # ------------------------- Point Mode -------------------------
        self.radio_point = RadioButton(canvas=self.canvas_field, x=550, y=437.5, r=14, active_color=Color.blue, inactive_color=Color.lightgray, text="Point Mode", font_name="Inter-Regular", text_size=font_size_button_small, on_default=False)
        self.text_z_point = TextBox(canvas=self.canvas_field, x=540, y=495, text="z-axis position", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.text_z_entry = Entry(master=self, canvas=self.canvas_field, x=480, y=520.5, w=100, h=30, color=Color.blue)
        self.text_z_point_mm = TextBox(canvas=self.canvas_field, x=600, y=532.5, text="mm", font_name="Inter-SemiBold", font_size=font_size_detail, color=Color.darkgray, anchor="center")
        self.text_z_point.hide()
        self.text_z_entry.hide()
        self.text_z_point_mm.hide()

        # ---------------------------------- Group movement ----------------------------------
        self.text_movement = TextBox(canvas=self.canvas_field, x=540, y=619.5, text="Movement", font_name="Inter-SemiBold", font_size=font_size_subtitle, color=Color.darkgray, anchor="center")
        self.press_home = PressButton(canvas=self.canvas_field, x=465, y=655, w=150, h=30, r=15, active_color=Color.gray, inactive_color=Color.lightgray, text="Home", font_name="Inter-SemiBold", text_size=font_size_button_home, active_default=True)
        self.press_run  = PressButton(canvas=self.canvas_field, x=465, y=695, w=150, h=35, r=15, active_color=Color.blue, inactive_color=Color.lightgray, text="Run", font_name="Inter-SemiBold", text_size=font_size_button_run, active_default=False)
        self.running = False
        self.homing = False

        # ---------------------------------- Error ----------------------------------
        self.message_error = MessageBox(canvas=self.canvas_field, x=380, y=460, width_field=320, text="", color=Color.red, align="Center", font_name="Inter-Bold", size=font_size_message_error)
        self.message_error.hide()

        # ---------------------------------- Connection ----------------------------------
        self.message_connection = MessageBox(canvas=self.canvas_field, x=380, y=630, width_field=320, text="\" Connection Disconnected \"", color=Color.red, align="Center", font_name="Inter-Bold", size=font_size_message_error)
        self.message_connection.hide()


        self.dot = None
        self.dot_point = None
        self.target_x = 0
        self.previous_x = 0
        self.previous_z = 0
        self.first_out_entry_flag = False
        self.first_point_entry_flag = False
        self.grid_flag = False
        self.dot_shelve_1 = None
        self.dot_shelve_2 = None
        self.dot_shelve_3 = None
        self.dot_shelve_4 = None
        self.dot_shelve_5 = None
        self.after_idle_flag = 0
        self.finish_run_flag = 2
        self.press_run_flag = False
        
        self.bind("<Return>", self.out_entry)
        self.canvas_field.bind("<Button-1>", self.handle_press_home)
        self.canvas_field.bind("<Button-1>", self.handle_press_run)
        self.canvas_field.bind("<Button-1>", self.out_entry)
    
    def handle_radio_operation(self):
        """
        This function handles when user press radio button (choose operation mode)
        """
        # Click Point Mode
        if self.operation_mode == "Jog" and self.radio_point.on:
            self.grid.delete_point(self.dot_point)
            self.grid.delete_all_dots()
            self.radio_jog.turn_off()
            self.operation_mode = "Point"
            self.text_pick.hide()
            self.text_place.hide()
            self.press_set_shelves.hide()

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
            self.text_z_entry.set_text("0")
            self.first_out_entry_flag = False
            self.first_point_entry_flag = False
            self.grid_flag = False
            
        # Click Jog Mode
        elif self.operation_mode == "Point" and self.radio_jog.on:
            self.grid.delete_point(self.dot_point)
            self.radio_point.turn_off()
            self.operation_mode = "Jog"
            self.text_pick.show()
            self.text_place.show()
            self.press_set_shelves.show()

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
            self.protocol_z.vacuum = "1"
        elif self.mode == "Protocol":
            self.protocol_z.write_vaccuum_status("Vacuum On")
        self.toggle_vacuum.turn_on()
    
    def turn_off_vacuum(self):
        """
        This function turns off vacuum with protocol, turn off vacuum toggle, hide vacuum on UI's navigator
        """
        if self.mode == "Graphic":
            self.protocol_z.vacuum = "0"
        elif self.mode == "Protocol":
            self.protocol_z.write_vaccuum_status("Vacuum Off")
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

    def turn_on_movement(self):
        """
        This function turns on movement with protocol, turn on movement toggle, show movement on UI's navigator
        """
        if self.mode == "Graphic":
            self.protocol_z.gripper = "1"
        elif self.mode == "Protocol":
            self.protocol_z.write_gripper_status("Movement Forward")
        self.toggle_movement.turn_on()
    
    def turn_off_movement(self):
        """
        This function turns off movement with protocol, turn off movement toggle, hide movement on UI's navigator
        """
        if self.mode == "Graphic":
            self.protocol_z.gripper = "0"
        elif self.mode == "Protocol":
            self.protocol_z.write_gripper_status("Movement Backward")
        self.toggle_movement.turn_off()
    
    def handle_toggle_movement(self):
        """
        This function handles when user press movement toggle
        """
        if self.toggle_movement.pressed:
            # Turn movement On
            if not self.toggle_movement.on:
                self.turn_on_movement()
            # Turn movement Off
            else:
                self.turn_off_movement()
            self.toggle_movement.pressed = False
    
    def out_entry(self, event):
        """
        This function is called when user click outside the entry or press enter or click on the grid
        """
        if self.operation_mode == "Point":
            print(self.validate_entry)
            # Move Target according to Entry's value if value is normal 
            if self.validate_entry() == "Normal":

                if self.text_z_entry.get_value():
                    self.target_z = self.text_z_entry.get_value()
                    # print("\n-------- DEBUG --------")
                    # print("previous x: ", self.previous_x)
                    # print("previous z: ",self.previous_z)
                    # print("target_z: ", self.target_z)
                    # print("target_x: ", self.target_x)

                    # condition when click out of entry first when in point mode
                    if not self.first_out_entry_flag:
                        self.target_x, self.target_z, self.dot = self.grid.show_point(self.target_z, self.operation_mode)
                        self.dot_point = self.dot
                        self.point_target_z = self.target_z
                        self.point_target_x = self.target_x
                        self.first_out_entry_flag = True
                        # print(f"Position first is (x={self.point_target_x }, z={self.point_target_z})")

                    # condition when click out or type in entry 
                    if self.previous_x != self.target_x and self.previous_z != self.target_z:
                        self.target_x, self.target_z, self.dot = self.grid.show_point(self.target_z, self.operation_mode)
                        self.previous_x = self.target_x
                        self.previous_z = self.target_z
                        self.dot_point = self.dot
                        if isinstance(self.target_x, int) and isinstance(self.target_z, int):
                            self.point_target_z = self.target_z
                            self.point_target_x = self.target_x
                            self.text_z_entry.set_text(str(self.previous_z))
                            # print(f"Position 1 is (x={self.point_target_x}, z={self.point_target_z})")

                    # condition incase type in the entry
                    elif self.previous_x == self.target_x and self.previous_z != self.target_z:
                        self.target_x, self.target_z, self.dot = self.grid.show_point(self.target_z, self.operation_mode)
                        self.previous_x = self.target_x
                        self.previous_z = self.target_z
                        self.dot_point = self.dot
                        if isinstance(self.target_x, int) and isinstance(self.target_z, int):
                            self.point_target_z = self.target_z
                            self.point_target_x = self.target_x
                            self.text_z_entry.set_text(str(self.previous_z))
                            # print(f"Position 3 is (x={self.point_target_x}, z={self.point_target_z})")
                
                    # When click on grid
                    self.target_x, self.target_z, self.dot, self.grid_flag = self.grid.on_click(event, self.operation_mode)
                    
                    if self.grid_flag:
                        self.previous_x = self.target_x
                        self.previous_z = self.target_z
                        self.grid_flag = False
                        self.dot_point = self.dot
                        if isinstance(self.target_x, int) and isinstance(self.target_z, int):
                            self.point_target_z = self.target_z
                            self.point_target_x = self.target_x
                            self.text_z_entry.set_text(str(self.previous_z))
                            # print(f"Position grid is (x={self.point_target_x}, z={self.point_target_z})")

                    print(f"Final position is (x={self.point_target_x}, z={self.point_target_z})")

        if self.operation_mode == "Jog":    
            if not self.running and not self.homing and not self.jogging and not self.gripping and not self.vacuum:
                self.focus()
                self.order_pick_1 = self.entry_pick_1.get_value()
                self.order_pick_2 = self.entry_pick_2.get_value()
                self.order_pick_3 = self.entry_pick_3.get_value()
                self.order_pick_4 = self.entry_pick_4.get_value()
                self.order_pick_5 = self.entry_pick_5.get_value()

                self.order_place_1 = self.entry_place_1.get_value()
                self.order_place_2 = self.entry_place_2.get_value()
                self.order_place_3 = self.entry_place_3.get_value()
                self.order_place_4 = self.entry_place_4.get_value()
                self.order_place_5 = self.entry_place_5.get_value()

                # Debug
                order_1 = f"{self.order_pick_1} to {self.order_place_1}"
                order_2 = f"{self.order_pick_2} to {self.order_place_2}"
                order_3 = f"{self.order_pick_3} to {self.order_place_3}"
                order_4 = f"{self.order_pick_4} to {self.order_place_4}"
                order_5 = f"{self.order_pick_5} to {self.order_place_5}"
                # order = {"order_1": {order_1}, "order_2": {order_2}, "order_3": {order_3}, "order_4": {order_4}, "order_5": {order_5}}
                # print(f"order: {order}")


    def validate_entry(self):
        """
        This function validates input in entry and show error message
        """
        if self.operation_mode == "Point": 
            # Get value from Entry
            self.z_value = self.text_z_entry.get_value()
            # Validate Entry's Value
            validate_x_result = self.text_z_entry.validate(self.z_value)
            # Interpret Validation Result
            validate_point_result = "Normal"
            if validate_x_result  != 0:
                self.text_z_entry.error() # Entry Error (Red Text)
                validate_point_result = self.interpret_validate(validate_x_result, self.operation_mode)
            else:
                self.text_z_entry.normal()

            # Display Error Message if Entry Error
            if validate_point_result != "Normal":
                self.message_error.change_text(validate_point_result)
                self.message_error.show()
                self.press_run.deactivate()
            else:
                self.message_error.hide()
                if self.mode == "Graphic" and not self.running and not self.homing and not self.jogging and not self.gripping and self.connection:
                    self.press_run.activate()
                elif not self.running and not self.homing and not self.jogging and not self.gripping and self.connection and self.protocol_z.usb_connect and self.protocol_z.routine_normal:
                    self.press_run.activate()
            return validate_point_result
        else:
            self.message_error.hide()
            if not self.running and not self.homing and not self.jogging and not self.gripping and self.connection:
                self.press_run.activate()
          
    def interpret_validate(self, validate_result, operation_mode):
        """
        This function converts number code from validation result to error text
        """
        if self.operation_mode == "Point":
            if validate_result == 1:
                return Error.code_point_1
                    
    def handle_press_home(self):
        """
        This function handles when user press "Home" button
        """
        if self.press_home.pressed:
            print(f"press Home")
            if self.mode == "Graphic":
                self.protocol_z.z_axis_moving_status = "Home"
            elif self.mode == "Protocol":
                self.protocol_z.write_base_system_status("Home")
            self.homing = True
            self.toggle_vacuum.deactivate()
            self.toggle_movement.deactivate()
            
            self.radio_jog.deactivate()  
            self.entry_pick_1.disable()
            self.entry_pick_2.disable()
            self.entry_pick_3.disable()
            self.entry_pick_4.disable()
            self.entry_pick_5.disable()

            self.entry_place_1.disable()
            self.entry_place_2.disable()
            self.entry_place_3.disable()
            self.entry_place_4.disable()
            self.entry_place_5.disable()  

            self.radio_point.deactivate()
            self.text_z_entry.disable()      
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_home.pressed = False
    
    def handle_press_run(self):
        """
        This function handles when user press "Run" button
        """
        if self.press_run.pressed:
            if self.operation_mode == "Jog":
                if self.mode == "Graphic":
                    self.protocol_z.z_axis_moving_status = "pick"
                elif self.mode == "Protocol":
                    #Combine Order pick and place
                    self.pick_out =  int(f"{self.order_pick_1}{self.order_pick_2}{self.order_pick_3}{self.order_pick_4}{self.order_pick_5}")
                    self.place_out = int(f"{self.order_place_1}{self.order_place_2}{self.order_place_3}{self.order_place_4}{self.order_place_5}")
                    print(self.pick_out,self.place_out)
                    self.protocol_z.write_pick_place_order(self.pick_out,self.place_out)
                    self.protocol_z.write_base_system_status("Run Jog Mode")
            elif self.operation_mode == "Point":
                if self.mode == "Graphic":
                    self.protocol_z.z_axis_moving_status = "Go Point"
                elif self.mode == "Protocol":
                    self.protocol_z.write_goal_point(self.point_target_z)
                    self.protocol_z.write_base_system_status("Run Point Mode")
            self.running = True

            self.toggle_vacuum.deactivate()
            self.toggle_movement.deactivate()
            
            self.radio_jog.deactivate()  
            self.entry_pick_1.disable()
            self.entry_pick_2.disable()
            self.entry_pick_3.disable()
            self.entry_pick_4.disable()
            self.entry_pick_5.disable()

            self.entry_place_1.disable()
            self.entry_place_2.disable()
            self.entry_place_3.disable()
            self.entry_place_4.disable()
            self.entry_place_5.disable()

            self.press_set_shelves.deactivate()
            self.radio_point.deactivate()
            self.text_z_entry.disable()  
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_run.pressed = False
            self.press_run_flag = True

    def handle_press_set_shelves(self):
        """
        This function handles when user press "Set Set Shelves" button
        """
        if self.press_set_shelves.pressed:
            # Close Vacuum & Backward Movement First
            
            if self.toggle_movement.on:
                # print("still pressed move")
                self.toggle_movement.pressed = False
                self.turn_off_movement()
            if self.toggle_vacuum.on:
                # print("still pressed vac")
                self.toggle_vacuum.pressed = False
                self.turn_off_vacuum()

            self.operation_mode = 'Point'
            self.grid.delete_all_dots()

            self.operation_mode = 'Jog'

            if self.mode == "Graphic":
                self.protocol_z.z_axis_moving_status = "Set Shelves"
            elif self.mode == "Protocol":
                self.protocol_z.write_base_system_status("Set Shelves")
            self.jogging = True
            self.toggle_vacuum.deactivate()
            self.toggle_movement.deactivate()
            
            self.radio_jog.deactivate()
            self.entry_pick_1.disable()
            self.entry_pick_2.disable()
            self.entry_pick_3.disable()
            self.entry_pick_4.disable()
            self.entry_pick_5.disable()

            self.entry_place_1.disable()
            self.entry_place_2.disable()
            self.entry_place_3.disable()
            self.entry_place_4.disable()
            self.entry_place_5.disable()

            self.radio_point.deactivate()
            self.press_set_shelves.deactivate()
            self.text_z_entry.disable()  
            self.press_run.deactivate()
            self.press_home.deactivate()
            self.press_set_shelves.pressed = False

    def handle_finish_moving(self):
        """
        This function handles when finish moving to reactivate elements
        """
        self.toggle_vacuum.activate()
        self.toggle_movement.activate()
            
        self.radio_jog.activate()  
        self.entry_pick_1.enable()
        self.entry_pick_2.enable()
        self.entry_pick_3.enable()
        self.entry_pick_4.enable()
        self.entry_pick_5.enable()

        self.entry_place_1.enable()
        self.entry_place_2.enable()
        self.entry_place_3.enable()
        self.entry_place_4.enable()
        self.entry_place_5.enable()  

        self.radio_point.activate()
        self.text_z_entry.enable()  
        self.press_set_shelves.activate()
        self.press_run.activate()
        self.press_run.activate()
        self.press_home.activate()
        self.press_run_flag = False

    def handle_connection_change(self):
        """
        This function handles when connection change
        """
        if self.connection != self.new_connection:
            # Update Connection Value
            self.connection = self.new_connection
            if not self.connection: # If Disconnected
                self.handle_disconnected()
            else: # If Reconnected
                self.handle_connected()

    def handle_disconnected(self):
        """
        This function handles when connection miss a heartbeat
        """
        self.message_connection.show()

        self.toggle_vacuum.deactivate()
        self.toggle_movement.deactivate()

        self.text_x_pos_num.deactivate(self.text_x_pos_num.text, Color.lightgray)
        self.text_z_pos_num.deactivate(self.text_z_pos_num.text, Color.lightgray)
        self.text_z_spd_num.deactivate(self.text_z_spd_num.text, Color.lightgray)
        self.text_z_acc_num.deactivate(self.text_z_acc_num.text, Color.lightgray)
        self.text_z_status_value.deactivate(self.text_z_status_value.text, Color.lightgray)
        
        self.radio_jog.deactivate()  
        self.entry_pick_1.disable()
        self.entry_pick_2.disable()
        self.entry_pick_3.disable()
        self.entry_pick_4.disable()
        self.entry_pick_5.disable()

        self.entry_place_1.disable()
        self.entry_place_2.disable()
        self.entry_place_3.disable()
        self.entry_place_4.disable()
        self.entry_place_5.disable()  

        self.radio_point.deactivate()
        self.text_z_entry.disable()  
        self.press_run.deactivate()
        self.press_home.deactivate()
        
    def handle_connected(self):
        """
        This function handles when connection obtain a heartbeat again
        """
        self.message_connection.hide()
        self.text_x_pos_num.activate(self.text_x_pos_num.text, Color.blue)
        self.text_z_pos_num.activate(self.text_z_pos_num.text, Color.blue)
        self.text_z_spd_num.activate(self.text_z_spd_num.text, Color.blue)
        self.text_z_acc_num.activate(self.text_z_acc_num.text, Color.blue)
        self.text_z_status_value.activate(self.text_z_status_value.text, Color.blue)

        if not self.running and not self.homing and not self.jogging:
            self.radio_jog.activate()  
            self.entry_pick_1.enable()
            self.entry_pick_2.enable()
            self.entry_pick_3.enable()
            self.entry_pick_4.enable()
            self.entry_pick_5.enable()

            self.entry_place_1.enable()
            self.entry_place_2.enable()
            self.entry_place_3.enable()
            self.entry_place_4.enable()
            self.entry_place_5.enable()  

            self.radio_point.activate()
            self.text_z_entry.enable()  
            self.press_run.activate()
            self.press_home.activate()
            self.press_run.activate()
            self.press_home.activate()

            self.toggle_movement.activate()
            self.toggle_vacuum.activate()

    def handle_ui_change(self):
        """
        This function handles updating UI (according to protocol status) 
        """ 
        
        # Actual Gripper 
        if self.protocol_z.gripper_actual_reed1 == "1":  
            self.status_reed_switch_1.change_text("ON", color=Color.blue)
        else:
            self.status_reed_switch_1.change_text("OFF", color=Color.gray)

        if self.protocol_z.gripper_actual_reed2 == "1":
            self.status_reed_switch_2.change_text("ON", color=Color.blue)
        else:
            self.status_reed_switch_2.change_text("OFF", color=Color.gray)
            
        # Actual motion value
        self.text_x_pos_num.change_text(self.protocol_z.x_axis_actual_pos)
        self.text_z_pos_num.change_text(self.protocol_z.z_axis_actual_pos)
        self.text_z_spd_num.change_text(self.protocol_z.z_axis_actual_spd)
        self.text_z_acc_num.change_text(self.protocol_z.z_axis_actual_acc)
        self.text_z_status_value.change_text(self.protocol_z.z_axis_moving_status)

        # Moving Status
        if self.protocol_z.z_axis_moving_status == "Idle":
            # When finish moving
            if self.protocol_z.z_axis_moving_status_before != "Idle":

                if (self.finish_run_flag == 0 or self.operation_mode == 'Point') and self.press_run_flag:
                    self.handle_finish_moving()
                    self.grid.delete_point(self.dot_point)
                    self.grid.delete_all_dots()
                    self.text_z_entry.set_text("0")
                    self.finish_run_flag = 1
                
                if self.press_home.pressed == False:
                    self.handle_finish_moving()
                    self.grid.delete_point(self.dot_point)
                    self.grid.delete_all_dots()
                    self.text_z_entry.set_text("0")

                if self.protocol_z.z_axis_moving_status_before == "Go Point":
                    self.running = False
                elif self.protocol_z.z_axis_moving_status_before == "Home":
                    self.homing = False
                elif self.protocol_z.z_axis_moving_status_before == "Go Pick":
                    self.running = False
                elif self.protocol_z.z_axis_moving_status_before == "Go Place":
                    self.running = False
                elif self.protocol_z.z_axis_moving_status_before == "Set Shelves":
                    if self.mode == "Protocol" and self.operation_mode == "Jog" and self.finish_run_flag != 1:
                        self.protocol_z.read_Shelve_position()
                        self.finish_run_flag = 0
                        self.handle_finish_moving()
                        self.target_z_1 = self.protocol_z.shelve_1
                        self.target_x, self.target_z_1, self.dot_shelve_1 = self.grid.show_point(int(self.target_z_1), self.operation_mode)
                        
                        self.target_z_2 = self.protocol_z.shelve_2
                        self.target_x, self.target_z_2, self.dot_shelve_2 = self.grid.show_point(int(self.target_z_2), self.operation_mode)
                        
                        self.target_z_3 = self.protocol_z.shelve_3
                        self.target_x, self.target_z_3, self.dot_shelve_3 = self.grid.show_point(int(self.target_z_3), self.operation_mode)
                        
                        self.target_z_4 = self.protocol_z.shelve_4
                        self.target_x, self.target_z_4, self.dot_shelve_4 = self.grid.show_point(int(self.target_z_4), self.operation_mode)
                        
                        self.target_z_5 = self.protocol_z.shelve_5
                        self.target_x, self.target_z_5, self.dot_shelve_5 = self.grid.show_point(int(self.target_z_5), self.operation_mode)
                    elif self.finish_run_flag == 1:
                        self.finish_run_flag = 2                       

                    self.jogging = False
                self.protocol_z.z_axis_moving_status_before = "Idle"

    def handle_protocol_z(self):
        """
        This function handles protocol y
        """
        # Check USB connection
        if self.protocol_z.usb_connect:
            # When reconnect USB
            if self.protocol_z.usb_connect_before == False:
                print("When reconnect USB")
                self.handle_connected()
                self.protocol_z.usb_connect_before = True
            # Check if there is protocol error from user (y-axis)
            if self.protocol_z.routine_normal == False:
                self.message_connection.change_text("Protocol Error from Z-Axis")
                self.handle_disconnected()
            else:
                # Do protocol as normal every 200 ms
                if self.time_ms_y >= 200:
                    self.time_ms_y = 0
                    self.new_connection = self.protocol_z.heartbeat()
                    if self.new_connection: # If Connected
                        self.protocol_z.routine() # Do routine
                    self.end_time = time.time()
                    self.print_current_activity()
                    print((self.end_time-self.start_time)*1000, "ms\n")
                    self.start_time = time.time()
                # If Connection is Changed 
                self.handle_connection_change()
                # Update UI accoring to protocol status
                self.handle_ui_change()
        else:
            self.message_connection.change_text("Please Connect the USB")
            self.handle_disconnected()
            self.protocol_z.write_heartbeat()
            self.protocol_z.usb_connect_before = False

    def print_current_activity(self):
        """
        This function prints current activity for debugging in terminal
        """
        if self.running:   print("Running")
        if self.homing:    print("Homing")
        if self.jogging:   print("Jogging Set Shelve")
        if self.vacuum:    print("Vacuum")

if __name__ == "__main__":
    app = App()
    app.task()
    app.mainloop()