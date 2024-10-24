import random
import time
import pyniryo2 as pyniryo
import numpy as np
import threading

#IP = "172.27.13.150"
#IP = "192.168.4.73"
IP = "localhost"

def move_arm_to_initial_position():
    return [0, 0.499, -1.248, 0, 0, 0]

def move_arm_to_grab_position():
    return [0.0, -0.5, -0.85, 0.0, 0.0, 0.0]


def main(robot: pyniryo.NiryoRobot) -> None:
    gripped = False
    robot.arm.calibrate_auto()
    while True:
        try:
            before = time.time()
            robot.arm.move_joints(move_arm_to_initial_position())
            robot.arm.move_joints(move_arm_to_grab_position())
            print("Movement time: " + str(time.time() - before))
            if not gripped:
                robot.tool.close_gripper()
                gripped = True
            else:
                robot.tool.open_gripper()
                gripped = False
            print("Total Time taken: " + str(time.time() - before))
        except Exception as e:
           print("The robot could not reach the requested position.")
           print("Error:", e)

if __name__ == '__main__':

    robot = pyniryo.NiryoRobot(IP) #192.168.10.178
    try:
        main(robot)
    except KeyboardInterrupt:
        print("Going to sleep, please wait...")
        robot.arm.go_to_sleep()
        # robot.pick_place.pick_from_pose(pos)
        print("The robot got stopped.")
        robot.end()

