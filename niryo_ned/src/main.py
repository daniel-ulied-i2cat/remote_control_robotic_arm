import time
import termios
import sys
import subprocess
import threading
import argparse

import pyniryo2 as pyniryo
import roslibpy

#from arm.arm_controller_control_based import ArmControllerPositionBased as ArmController
from arm.arm_controller_position_based import ArmControllerPositionBased as ArmController
from stdinout.stdin_out_controller import StdInOutController

IP = "172.27.13.150"
INITIAL_POSITION = [0, 0.499, -1.248, 0, 0, 0]
STEP_SIZE = 0.2
INITIAL_FIGURE_PATH = "./figures/motd-wrapper.py"
INITIAL_REMOTE_FIGURE_PATH = "./figures/remote-information.py"

def main(robot: pyniryo.NiryoRobot, arm_controller: ArmController) -> None:
    """
    Main function to control the Niryo Ned robot arm using the keyboard.

    Parameters
    ----------
    robot: pyniryo.NiryoRobot
        The NiryoRobot object to control the robot
    
    arm_controller: ArmController
        The ArmController object to control the robot arm
    
    Returns
    -------
    None
    """
    robot.arm.calibrate_auto()
    settings = termios.tcgetattr(sys.stdin)

    try:
        key_thread = threading.Thread(target=arm_controller.move_robot)
        key_thread.daemon = True
        key_thread.start()
    
        arm_controller.position_calculator()
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control Niryo Ned robot arm.')
    parser.add_argument('--docker', action='store_true', help='Specify if running in a Docker container')
    args = parser.parse_args()

    if args.docker:
        subprocess.run(INITIAL_REMOTE_FIGURE_PATH, encoding='utf-8')
    else:
        subprocess.run(INITIAL_FIGURE_PATH, encoding='utf-8')

    try:
        robot = pyniryo.NiryoRobot(IP)
    except roslibpy.core.RosTimeoutError:
        print("The robot is not connected. Please check the connection. \nIgnore the following error (it's a PyNiryo2 internal error).\n")
        sys.exit()

    arm_controller = ArmController(robot, INITIAL_POSITION, STEP_SIZE)
    std_in_out_controller = StdInOutController()
    original_settings = std_in_out_controller.disable_echo()

    try:
        main(robot, arm_controller)
    except KeyboardInterrupt:
        #time.sleep(2)
        robot.arm.go_to_sleep()
        print("\n\n\nThe robot got stopped.")
    finally:
        robot.end()
        std_in_out_controller.restore_terminal(original_settings)
