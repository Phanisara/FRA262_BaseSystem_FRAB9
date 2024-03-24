import platform
import struct
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.client import ModbusTcpClient

# ----------------------------------- Config this variable before using ----------------------------------- 
device_port = "COM3"
# example: for os -> device_port = "/dev/cu.usbmodem14103"
#          for window -> device_port = "COM3"
# ---------------------------------------------------------------------------------------------------------

class Binary():
    """
    Binary Class
    """
    def decimal_to_binary(self, decimal_num):
        """
        This function converts base 10 to base 2
        """
        binary_num = ""
        while decimal_num > 0:
            binary_num = str(decimal_num % 2) + binary_num
            decimal_num = decimal_num // 2
        # Fill to 16 digits with 0
        if len(binary_num) < 16:
            binary_num = "0"*(16-len(binary_num)) + binary_num
        return binary_num
        
    def binary_to_decimal(self, binary_num):
        """
        This function converts base 2 to base 10
        """
        decimal_num = 0
        for i in range(len(binary_num)):
            decimal_num += int(binary_num[i]) * (2 ** (len(binary_num)-i-1))
        return decimal_num
    
    def binary_crop(self, digit, binary_num):
        """
        This function crops the last n digits of the binary number
        """
        return binary_num[len(binary_num)-digit:]

    def binary_twos_complement(self, number):
        """
        This functions converts the (negative) number to its 16-bit two's complement representation
        """
        if number < 0:
            number = (1 << 16) + number  # Adding 2^16 to the negative number
        return number
    
    def binary_reverse_twos_complement(self, number):
        """
        This functions converts the 16-bit two's complement number back to its original signed representation 
        """
        if number & (1 << 15):  # Check if the most significant bit is 1
            number = number - (1 << 16)  # Subtract 2^16 from the number
        return number

class Protocol_Z(Binary):
    """
    Protocol Z Class
    """
    def __init__(self):
        self.os = platform.platform()[0].upper()
        if self.os == 'M': #Mac
            self.port = device_port
        elif self.os == 'W': #Windows        
            self.port = device_port

        self.usb_connect = False
        self.usb_connect_before = False

        self.slave_address = 0x15
        self.register = []
        
        self.routine_normal = True

        self.vacuum = "0"
        self.gripper = "0"

        self.z_axis_moving_status_before = "Idle"
        self.z_axis_moving_status = "Idle"
        self.z_axis_actual_pos = 0.0
        self.z_axis_actual_spd = 0.0
        self.z_axis_actual_acc = 0.0
        self.x_axis_actual_pos = 0.0

        self.shelve_1 = 0
        self.shelve_2 = 0
        self.shelve_3 = 0
        self.shelve_4 = 0
        self.shelve_5 = 0

        self.goal_point_x_register = 0

        self.client = ModbusClient(method="rtu", port=self.port, stopbits=1, bytesize=8, parity="E", baudrate=19200)
        print('Z-Axis Connection Status :', self.client.connect())

        self.write_heartbeat() # Write heartbeat as "Hi"
        
    def heartbeat(self):
        if self.read_hearbeat() == 22881: # Read heartbeat as "Ya"
            self.write_heartbeat() # Write heartbeat as "Hi"
            return True
        else:
            return False

    def routine(self):
        try:
            self.register = self.client.read_holding_registers(address=0x00, count=0x46, slave=self.slave_address).registers
            self.read_end_effector_status()
            self.read_z_axis_moving_status()
            self.read_z_axis_actual_motion()
            self.read_x_axis_actual_motion()
            print("Vacuum:", self.vacuum)
            print("Gripper:", self.gripper)
            print("Pos:", self.z_axis_actual_pos, "\tSpd:", self.z_axis_actual_spd, "\tAcc:", self.z_axis_actual_acc)
            print("Z-Axis Moving Status:", self.z_axis_moving_status)
            self.routine_normal = True
        except Exception as e:
            print("Routine Error", e)
            self.routine_normal = False

    def read_hearbeat(self):
        try:
            hearbeat_value = self.client.read_holding_registers(address=0x00, count=1, slave=self.slave_address).registers
        except Exception as e:
            print("Heartbeat Error", e)
            return "Error"
        return hearbeat_value[0]
    
    def write_heartbeat(self):
        try:
            self.client.write_register(address=0x00, value=18537, slave=self.slave_address)
            self.usb_connect = True
        except:
            self.usb_connect = False

    def write_base_system_status(self, command):
        if command == "Set Shelves":
            self.base_system_status_register = 0b0001
        elif command == "Home":
            self.base_system_status_register = 0b0010
        elif command == "Run Jog Mode":
            self.base_system_status_register = 0b0100
        elif command == "Run Point Mode":
            self.base_system_status_register = 0b1000
        self.client.write_register(address=0x01, value=self.base_system_status_register, slave=self.slave_address)
        print("Write Base System Status to Client")

    def read_end_effector_status(self):
        vacuum_status_binary = self.binary_crop(4, self.decimal_to_binary(self.register[0x02]))[::-1]
        gripper_status_binary = self.binary_crop(4, self.decimal_to_binary(self.register[0x03]))[::-1]
        self.vacuum = vacuum_status_binary[0]
        self.gripper = gripper_status_binary[0]

    def write_vaccuum_status(self, command):
        if command == "Vacuum On":
            self.end_effector_status_register = 0b0001
        elif command == "Vacuum Off":
            self.end_effector_status_register = 0b0000
        self.client.write_register(address=0x02, value=self.end_effector_status_register, slave=self.slave_address)

    def write_gripper_status(self, command):
        if command == "Movement Forward":
            self.end_effector_status_register = 0b0001
        elif command == "Movement Backward":
            self.end_effector_status_register = 0b0000
        self.client.write_register(address=0x03, value=self.end_effector_status_register, slave=self.slave_address)

    def write_pick_place_order(self, pick,place):
    
        self.client.write_register(address=0x21, value=pick, slave=self.slave_address)
        self.client.write_register(address=0x22, value=place, slave=self.slave_address)

    def read_z_axis_moving_status(self):
        self.z_axis_moving_status_before = self.z_axis_moving_status
        z_axis_moving_status_binary = self.binary_crop(6, self.decimal_to_binary(self.register[0x10]))[::-1]
        if z_axis_moving_status_binary[0] == "1":
            self.z_axis_moving_status = "Set Shelves"
        elif z_axis_moving_status_binary[1] == "1":
            self.z_axis_moving_status = "Home"
        elif z_axis_moving_status_binary[2] == "1":
            self.z_axis_moving_status = "Go Pick"
        elif z_axis_moving_status_binary[3] == "1":
            self.z_axis_moving_status = "Go Place"
        elif z_axis_moving_status_binary[4] == "1":
            self.z_axis_moving_status = "Go Point"
        else:
            self.z_axis_moving_status = "Idle"

    def read_z_axis_actual_motion(self):
        self.z_axis_actual_pos = self.binary_reverse_twos_complement(self.register[0x11]) / 10
        self.z_axis_actual_spd = self.register[0x12] / 10
        self.z_axis_actual_acc = self.register[0x13] / 10

    def read_x_axis_actual_motion(self):
        self.x_axis_actual_pos = self.binary_reverse_twos_complement(self.register[0x40]) / 10

    def write_goal_point(self, z):
        # self.goal_point_x_register = self.binary_twos_complement(int(x*10))
        self.goal_point_z_register = self.binary_twos_complement(int(z*10))
        # self.client.write_register(address=0x30, value=self.goal_point_x_register, slave=self.slave_address)
        self.client.write_register(address=0x30, value=self.goal_point_z_register, slave=self.slave_address)

    def read_Shelve_position(self):
        self.shelve_1 = self.binary_reverse_twos_complement(self.register[0x23]) / 10
        self.shelve_2 = self.binary_reverse_twos_complement(self.register[0x24]) / 10
        self.shelve_3 = self.binary_reverse_twos_complement(self.register[0x25]) / 10
        self.shelve_4 = self.binary_reverse_twos_complement(self.register[0x26]) / 10
        self.shelve_5 = self.binary_reverse_twos_complement(self.register[0x27]) / 10
        print("Shelve Readed")