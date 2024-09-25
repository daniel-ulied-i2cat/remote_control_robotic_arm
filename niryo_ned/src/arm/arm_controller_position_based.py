from __future__ import annotations

import sys
import time

import pyniryo2 as pyniryo
import roslibpy

from arm.arm_controller import ArmController
from stdinout.stdin_out_controller import StdInOutController

class ArmControllerPositionBased(ArmController):

    def __init__(self, robot: pyniryo.NiryoRobot, initial_position: list, step_size: float):
        super().__init__(robot, initial_position, step_size)
        self.action_pending = False
        self._print_joint_information()
        self.std_in_out_controller = StdInOutController()
        self.end = False

    def __action_finished(self, message: str) -> None:
        self.action_pending = False

    def _print_joint_information(self) -> None:
        sys.stdout.write("\n\n")
        sys.stdout.write(f"\r                      Base Motor   /  Shoulder Motor  /  Elbow Motor  /  Forearm Rotation Motor  /  Wrist Motor   /  Hand Rotation Motor  /        Grasp\n")
        sys.stdout.write(f"\r                    (-2.99 / 2.99) / (-1.83 / 0.61)   / (-1.34/1.57)  /      (-2.09 / 2.09)      / (-1.92 / 1.92) /    (-2.53 / 2.53)     /   (closed / open)\n")
        sys.stdout.flush()

    def _print_pos_information(self, pos: list[str]) -> None:
        sys.stdout.write(f"\rCurrent Position is:    {float(self.robot.arm.joints[0]):.2f}       /      {float(self.robot.arm.joints[1]):.2f}        /     {float(self.robot.arm.joints[2]):.2f}     /           {float(self.robot.arm.joints[3]):.2f}           /        {float(self.robot.arm.joints[4]):.2f}    /          {float(self.robot.arm.joints[5]):.2f}         /        {str(self.grasp)}\n")
        sys.stdout.write(f"\rTarget Position is:     {float(pos[0]):.2f}       /      {float(pos[1]):.2f}        /     {float(pos[2]):.2f}     /           {float(pos[3]):.2f}           /        {float(pos[4]):.2f}    /          {float(pos[5]):.2f}         /        {str(self.grasp)}\n")
        sys.stdout.write(f"\033[F\033[F")
        sys.stdout.flush()

    def position_calculator(self) -> None:
        """
        Thread Function to get the new key pressed by the user

        Parameters
        ----------
        key: str
            The key pressed by the user

        Returns
        -------
        None
        """
        while True:
            # wait for new key
            key = self.std_in_out_controller.get_key()
            if key == 'q':
                self.end = True
                raise KeyboardInterrupt  # Exit loop if 'q' is pressed
            
            # update the position list based on the key
            try:
                _, joint_index = self.actions[key]
                self.pos, _ = self._recalculate_position(key, joint_index)
            except KeyError:
                pass

    def move_robot(self) -> bool:
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
        while True:
            if self.end:
                break
            self._print_pos_information(self.pos)
            if not self.action_pending:
                # Function to move the robot arm
                self.action_pending = True
                time_before_command = time.time()
                self.robot.arm.move_joints(self.pos, self.__action_finished)
                time_taken = time.time() - time_before_command 