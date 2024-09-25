from __future__ import annotations

import sys
import time

import pyniryo2 as pyniryo

from stdinout.stdin_out_controller import StdInOutController
from arm.arm_controller import ArmController

class ArmControllerPositionBased(ArmController):

    def __init__(self, robot: pyniryo.NiryoRobot, initial_position: list, step_size: float):
        super().__init__(robot, initial_position, step_size)
    
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
            self.pos, step = self._recalculate_position(key, joint_index)

            self._print_moving_animation()

            time_before_command = time.time()
            self.robot.arm.move_joints(self.pos)
            time_taken = time.time() - time_before_command

            self._print_move_robot_summary(joint_name, step, time_taken)