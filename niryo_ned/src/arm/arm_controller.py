from __future__ import annotations

import sys
import time

import pyniryo2 as pyniryo

from stdinout.stdin_out_controller import StdInOutController

class ArmController:

    def __init__(self, robot: pyniryo.NiryoRobot, initial_position: list, step_size: float):
        self.robot = robot
        self.pos = initial_position
        self.step_size = step_size
        self.grasp = False
        self.key_count = 1
        self.actions = {
            'i': ("Shoulder", 1),
            'k': ("Shoulder", 1),
            'l': ("Base", 0),
            'j': ("Base", 0),
            'w': ("Elbow", 2),
            's': ("Elbow", 2),
            'a': ("Forearm", 3),
            'd': ("Forearm", 3),
            'r': ("Wrist", 4),
            'f': ("Wrist", 4),
            ' ': ("Grip", 5),
        }
        self.std_in_out_controller = StdInOutController()
    
    def _recalculate_position(self, key: str, joint_index: int) -> tuple[list[str], int]:

        # Calculate the step based on the key count
        step = self.step_size * self.key_count

        # Update position based on the action
        if key in ['i', 'k']:
            self.pos[joint_index] += step if key == 'k' else -step
        elif key in ['l', 'j']:
            self.pos[joint_index] += step if key == 'j' else -step
        elif key in ['w', 's']:
            self.pos[joint_index] += step if key == 'w' else -step
        elif key in ['a', 'd']:
            self.pos[joint_index] += -step if key == 'a' else step
        elif key in ['r', 'f']:
            self.pos[joint_index] += -step if key == 'a' else step
        elif key == ' ':
            if self.grasp:
                self.robot.tool.open_gripper()
                self.grasp = False
            else:
                self.robot.tool.close_gripper()
                self.grasp = True

        # Enforce joint limits
        self.pos[0] = max(-2.99, min(2.99, self.pos[0]))
        self.pos[1] = max(-1.83, min(0.61, self.pos[1]))
        self.pos[2] = max(-1.34, min(1.57, self.pos[2]))
        self.pos[3] = max(-2.09, min(2.09, self.pos[3]))
        self.pos[4] = max(-1.92, min(1.92, self.pos[4]))
        self.pos[5] = max(-2.53, min(2.53, self.pos[5]))
        
        return self.pos, step

    def _print_moving_animation(self) -> None:
        sys.stdout.write(f"\rMoving...                                                ")
        sys.stdout.flush()
        self.std_in_out_controller.animate()

    def _print_move_robot_summary(self, joint_name: str, step: float, time_taken: int) -> None:
        # Print the moved message
        sys.stdout.write("\n")
        sys.stdout.write(f"\rMoved {joint_name} by {step:.2f} in {time_taken:.2f} seconds.\n")
        sys.stdout.flush()
        sys.stdout.write(f"\033[F\033[F")  # Move cursor up two lines

    def move_robot(self, key: str) -> bool:
        pass
    