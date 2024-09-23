import random
import time
import pyniryo2 as pyniryo
from pyniryo2 import NiryoRobot, PoseObject
import numpy as np

IP = "172.27.13.150"

def main(robot: NiryoRobot) -> None:
    """
    Main function uses saved poses to move robot
    """
    pick_pose = PoseObject(
    x=0.30, y=0.0, z=0.15,
    roll=0, pitch=1.57, yaw=0.0
    )
    first_place_pose = PoseObject(
        x=0.0, y=0.2, z=0.15,
        roll=0, pitch=1.57, yaw=0.0
    )
    for i in range(5):
        robot.arm.move_pose(pick_pose)
        new_place_pose = first_place_pose.copy_with_offsets(x_offset=0.05 * i)
        robot.arm.move_pose(new_place_pose)


if __name__ == '__main__':
    robot = pyniryo.NiryoRobot(IP)
    try:
        main(robot)
    except KeyboardInterrupt:
        robot.arm.go_to_sleep()
        print("The robot got stopped.")
        robot.end()

