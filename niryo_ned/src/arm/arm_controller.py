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
    
    def move_robot(self, key: str) -> bool:
        """
        The following keys are used to control the robot arm:
            joint0: Base Motor
            - Controls the rotation of the robot's base
            - Positive Values (>-2.99): Rotate right
            - Negative Values (<2.99): Rotate left
            
            joint1: Shoulder Motor
            - Moves the shoulder of the robot arm
            - Positive Values (>-1.83): Raise the shoulder upward
            - Negative Values (<0.61): Lower the shoulder downward
            
            joint2: Elbow Motor
            - Moves the elbow of the robot arm
            - Positive Values (>-1.34): Raise the elbow upward
            - Negative Values (<1.57): Lower the elbow downward
            
            joint3: Forearm Rotation Motor
            - Rotates the wrist of the robot arm
            - Positive Values (>-2.09): Rotate wrist to the right
            - Negative Values (<2.09): Rotate wrist to the left
            
            joint4: Wrist Motor
            - Moves the fingers of the robot up and down
            - Positive Values (>-1.92): Move fingers upward
            - Negative Values (<1.92): Move fingers downward
            
            joint5: Hand Rotation Motor
            - Rotates or actuates the end effector or gripper
            - Positive Values (>-2.53): Rotate the gripper to the right
            - Negative Values (<2.53): Rotate the gripper to the left
        
            Parameters
            ----------
            key: str
                The key pressed by the user
            
            Returns
            -------
            bool
                True if the robot arm is moved, False otherwise
         """

        if key in self.actions:
            joint_name, joint_index = self.actions[key]

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
                if grasp:
                    self.robot.tool.open_gripper()
                    grasp = False
                else:
                    self.robot.tool.close_gripper()
                    grasp = True

            # Enforce joint limits
            self.pos[0] = max(-2.99, min(2.99, self.pos[0]))
            self.pos[1] = max(-1.83, min(0.61, self.pos[1]))
            self.pos[2] = max(-1.34, min(1.57, self.pos[2]))
            self.pos[3] = max(-2.09, min(2.09, self.pos[3]))
            self.pos[4] = max(-1.92, min(1.92, self.pos[4]))
            self.pos[5] = max(-2.53, min(2.53, self.pos[5]))

            # Print moving animation
            sys.stdout.write(f"\rMoving...                                                ")
            sys.stdout.flush()
            self.std_in_out_controller.animate()

            # Move the robot
            time_before_command = time.time()
            self.robot.arm.move_joints(self.pos)
            time_taken = time.time() - time_before_command

            # Print the moved message
            sys.stdout.write(f"\rMoved {joint_name} by {step:.2f} in {time_taken:.2f} seconds.\n")
            sys.stdout.flush()
            sys.stdout.write(f"\033[F")  # Move cursor up one line

        elif key == 'q':
            raise InterruptedError  # Exit loop if 'q' is pressed