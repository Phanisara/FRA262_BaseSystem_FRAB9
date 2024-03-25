# FRA262_BaseSystem_FRAB9
The base system with user interface for FRA262 (Robotics Studio III) pick & place robot axis Z project.

$~$

## Installation
1. Install all fonts that are in `/font` in your computer
2. Install the libraries by using following command
```bash
cd code && pip install -r requirements.txt
```
$~$

## Configuration 
You might need to change **`device_port`** same as display in Device Manager the **`protocal.py`** file.

$~$

## How to use
The most basic way to run base system is by running **main.py`** on the Visual Studio Code.
```bash
cd code && python main.py
```
The base system has 2 modes for command the robot
1. **Jog mode**
    When using this mode, first click `set shelves` button and then save the position of the shelves in the station of the base system by setting the bottom shelf to 1, and subsequently number the shelves accordingly up to the top shelf, which is 5. Then, input the order of pick and place for 5 orders, and finally click `Run` button.
2. **Point mode**
    When using this mode, you have the option to either click on the grid in the left block to set the position of axis Z that you want to go, or you can manually type the position of axis Z in the entry. If you click on the grid, the position X follows the grid range of -10 to 10. However, if you manually type the position of axis Z in the entry, the position X is set to 0.

$~$

## Testing Method
1. The system inspector selects the positions of the shelves, setting up 5 shelves.
2. You click `set shelves` button for starting the jogging.
2. Then, you jog each shelf position and save to the microcontroller. The bottom shelf is set to 1, and subsequent shelves are numbered accordingly up to the top shelf, which is 5.
3. The system inspector places the box on the shelf (either two or three boxes).
4. Then, the system inspector will randomly select the order of pick and place based on the boxes that are on the shelves.
    - Example:
        - In case two boxes
            - The system inspector places the boxes on shelves 1 and 4.
            - The orders of pick and place follow the picture below

            ![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_example2box.png?raw=true)
            
        - In case three boxes
            - The system inspector places the boxes on shelves 2, 4, and 5.
            - The orders of pick and place follow the picture below

            ![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_example3box.png?raw=true)

5. After setting up the shelves and placing the boxes, clicks "run" on the UI and check the output of working.

$~$

## Protocal : Address & Function 
### Register Address
| Address | Descriptions              | Operation   |
| ------- | -------------------------| ----------- |
| 0x00    | Heartbeat Protocol       | Read/Write  |
| 0x01    | Base System Status       | Write       |
| 0x02    | Vacuum Status            | Read/Write  |
| 0x03    | Movement Status          | Read/Write  |
| 0x04	  | Movement Actual Status 	 | Read
| 0x10    | z-axis Moving Status     | Read        |
| 0x11    | z-axis Actual Position   | Read        |
| 0x12    | z-axis Actual Speed      | Read        |
| 0x13    | z-axis Actual Acceleration | Read      |
| 0x21    | Pick Order               | Write       |
| 0x22    | Place Order              | Write       |
| 0x23    | 1st Shelves Postition    | Read        |
| 0x24    | 2nd Shelves Postition    | Read        |
| 0x25    | 3rd Shelves Postition    | Read        |
| 0x26    | 4th Shelves Postition    | Read        |
| 0x27    | 5th Shelves Postition    | Read        |
| 0x30    | Goal Point z             | Write       |
| 0x40    | x-axis Actual Position   | Read/Write  |

### Bit Postition
High Byte
| 15 | 14 | 13 | 12 | 11 | 10 | 9 | 8 |
| -- | -- | -- | -- | -- | -- | -- | -- |

Low Byte
| 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| -- | -- | -- | -- | -- | -- | -- | -- |

### Data Format
1. **Base System Status(0x01)**

| Bit | Data in Binary          | Data in Decimal | Meaning         |
|-----|-------------------------|-----------------|-----------------|
| 0   | 0000 0000 0000 0001    | 1               | Set Shelves     |
| 1   | 0000 0000 0000 0010    | 2               | Home            |
| 2   | 0000 0000 0000 0100    | 4               | Run Jog Mode    |
| 3   | 0000 0000 0000 1000    | 8               | Run Point Mode  |
> Example: If if you press `Home` button in Base system, it will change data in 2nd bit from 0 to 1 in address Base System Status(0x01).

2. **Vacuum Status(0x02)**

| Bit | Data in Binary                                     | Data in Decimal          | Meaning        |
|-----|----------------------------------------------------|--------------------------|----------------|
| 0   | 0000 0000 0000 0000 = Off                          | 0 = Off                  | Vacuum Off     |
| 0   | 0000 0000 0000 0001 = On                           | 1 = On                   | Vacuum On      |

> Example: If if you press `Toggle On Vaccum` in Base system, it will change data in 1st bit from 0 to 1 in address Vacuum Status(0x02).

3. **Gripper Movement Status(0x03)**

| Bit | Data in Binary                          | Data in Decimal             | Meaning                     |
|-----|-----------------------------------------|-----------------------------|-----------------------------|
| 0   | 0000 0000 0000 0000 = Backward         | 0 = Backward                | Movement Backward           |
| 0   | 0000 0000 0000 0001 = Forward          | 1 = Forward                 | Movement Forward            |

> Example: If if you press `Toggle Forward Movement` in Base system, it will change data in 1st bit from 0 to 1 in address Gripper Movement Status(0x03).

4. **Gripper Movement Actual Status (0x04)**

| Bit | Data in Binary                                                   | Data in Decimal | Meaning                |
|-----|-------------------------------------------------------------------|-----------------|------------------------|
| 0   | 0000 0000 0000 0000 = Lead Switch 2 Off, 0000 0000 0000 0001 = Lead Switch 2 On | 0 = Off, 1 = On  | Lead Switch 2 Status  |
| 1   | 0000 0000 0000 0000 = Lead Switch 1 Off, 0000 0000 0000 0010 = Lead Switch 1 On | 0 = Off, 2 = On  | Lead Switch 1 Status  |

In the cylinders of the gripper their will be 2 lead switch to providing feedback about the position of the piston within the cylinders for showing the forward/backward status of the gripper and that feedback movement need to show at the Base system.
> Example: If value is written '0b0001' in Gripper Movement Actual Status (0x04), the base system will show lead switch 1: off and lead switch 1: on.
>          If value is written '0b0010' in Gripper Movement Actual Status (0x04), the base system will show lead switch 1: on and lead switch 1: off.

5. **Z-axis Moving Status(0x10)**

| Bit | Data in Binary | Data in Decimal | Meaning    |
|-----|----------------|-----------------|------------|
| 0   | 0001           | 1               | Set Shelve |
| 1   | 0010           | 2               | Home       |
| 2   | 0100           | 4               | Go Pick    |
| 3   | 1000           | 8               | Go Place   |
| 4   | 1 0000         | 16              | Go Point   |

6. **Position / Speed / Acceleration**
The position, speed, and acceleration sent to the base system should contain only one decimal place. Before sending the values to the Base system, multiply the actual value by 10.(Base_system_Value = Actual_Value * 10)
> Example: If the value of the position you want to send is '123.4', multiply it by 10 to get '1234', and send this value to the address z-axis Actual Position (0x11). This will appear in the Base system as '123.4'.

7. **Pick Order(0x21) , Place Order(0x22)**
The order of pick and place sent from the Base system to the Z-axis will correspond to the pick and place order displayed in the GUI.

![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_example_pick_place.png?raw=true)

> Example: For the given image, the pick order is '53214', and the place order is '14352'.

$~$

## Base System Protocol Flow
1. **Heartbeat**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_heartbeat.png?raw=true)

2. **Routine**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_routine.png?raw=true)

3. **Vacuum On/Off**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_vacuum.png?raw=true)

4. **Gripper Movement Forward/Backward**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_gripper.png?raw=true)

5. **Set Shelves**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_set_shelves.png?raw=true)

6. **Set Goal Point**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_set_goal.png?raw=true)

7. **Run Point Mode**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_run_point_mode.png?raw=true)

8. **Set Home**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_set_home.png?raw=true)

9. **Set Pick/Place Order**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_set_pick_place.png?raw=true)

10. **Run Jog Mode**
![alt text](https://github.com/Phanisara/FRA262_BaseSystem_FRAB9/blob/main/img/readme_run_jog_mode.png?raw=true)