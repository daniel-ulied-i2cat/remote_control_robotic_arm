import time
import pyniryo2 as pyniryo
import termios
import sys
import subprocess
import threading

#from arm.arm_controller_control_based import ArmControllerPositionBased as ArmController
from arm.arm_controller_position_based import ArmControllerPositionBased as ArmController
from stdinout.stdin_out_controller import StdInOutController

IP = "172.27.13.150"
INITIAL_POSITION = [0, 0.499, -1.248, 0, 0, 0]
STEP_SIZE = 0.2
INITIAL_FIGURE_PATH = "./figures/motd-wrapper.py"


def main(robot: pyniryo.NiryoRobot) -> None:
    """
    Main function to control the Niryo Ned robot arm using the keyboard.

    Parameters
    ----------
    robot: pyniryo.NiryoRobot
        The NiryoRobot object to control the robot
    
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
    subprocess.run(INITIAL_FIGURE_PATH, encoding='utf-8')
    robot = pyniryo.NiryoRobot(IP)
    
    arm_controller = ArmController(robot, INITIAL_POSITION, STEP_SIZE)
    std_in_out_controller = StdInOutController()
    original_settings = std_in_out_controller.disable_echo()

    try:
        main(robot)
    except KeyboardInterrupt:
        time.sleep(2)
        robot.arm.go_to_sleep()
        print("\n\n\nThe robot got stopped.")
    finally:
        robot.end()
        std_in_out_controller.restore_terminal(original_settings)
