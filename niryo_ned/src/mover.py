import random
import time
import pyniryo2 as pyniryo
import numpy as np

IP = "172.27.13.150"

def generate_random_positions():
    # Define the range and step
    start = -0.8
    stop = 0.8
    step = 0.01
    
    # Create an array from start to stop with the given step
    range_array = np.arange(start, stop + step, step)

    # Robot Joints Position Array Description:
        # pos[x] = [joint0, joint1, joint2, joint3, joint4, joint5]
        # where each element in the array represents:
        # 
        # joint0: Base Motor
        #   - Controls the rotation of the robot's base
        #   - Positive Values (>0): Rotate right
        #   - Negative Values (<0): Rotate left
        #
        # joint1: Shoulder Motor
        #   - Moves the shoulder of the robot arm
        #   - Positive Values (>0): Raise the shoulder upward
        #   - Negative Values (<0): Lower the shoulder downward
        #
        # joint2: Elbow Motor
        #   - Moves the elbow of the robot arm
        #   - Positive Values (>0): Raise the elbow upward
        #   - Negative Values (<0): Lower the elbow downward
        #
        # joint3: Wrist Motor
        #   - Rotates the wrist of the robot arm
        #   - Positive Values (>0): Rotate wrist to the right
        #   - Negative Values (<0): Rotate wrist to the left
        #
        # joint4: Finger Motor
        #   - Moves the fingers of the robot up and down
        #   - Positive Values (>0): Move fingers upward
        #   - Negative Values (<0): Move fingers downward
        #
        # joint5: Gripper Motor
        #   - Rotates or actuates the end effector or gripper
        #   - Positive Values (>0): Rotate the gripper to the right
        #   - Negative Values (<0): Rotate the gripper to the left
        # robot.arm.move_joints(pos)
    
    # Pick an object from a specific pose.
        # The pose is defined by coordinates and orientation: [x, y, z, roll, pitch, yaw].
        # x=0.2, y=0.0, z=0.1 specify the position in meters.
        # roll=0.0, pitch=1.57, yaw=0.0 specify the orientation in radians.
        # robot.pick_place.pick_from_pose([0.2, 0.0, 0.1, 0.0, 1.57, 0.0])

    # Place the object at a new pose.
        # Similar to the pick function, the pose is defined by [x, y, z, roll, pitch, yaw].
        # x=0.0, y=0.2, z=0.1 position the robot arm in meters to the desired placement location.
        # roll=0.0, pitch=1.57, yaw=0.0 maintain the orientation of the end effector during placement.
        # robot.pick_place.place_from_pose([0.0, 0.2, 0.1, 0.0, 1.57, 0.0])

    return [random.choice(range_array) for _ in range(6)]

def main(robot: pyniryo.NiryoRobot) -> None:

    robot.arm.calibrate_auto()
    
    # print("Creating http server")
    # # Start the Prometheus HTTP server on the specific IP address and port
    # start_http_server(8006)
    # pos1 = [0.0, -0.059, 1.170, 0.0, 0.0, 0.0]
    # pos2 = [0.0, 0.5, -1.251, 0.0, 0.0, 0.0]

    counter = 1
    while True:
        try:
            start_time = time.time()
            pos = generate_random_positions()
            # pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            # robot.pick_place.pick_from_pose(pos)
            robot.arm.move_joints(pos)            
            elapsed_time = time.time() - start_time
            time.sleep(2)
            #example_metric.set(elapsed_time)
            print(f"Position {counter}: {pos}")
            # print(f"Time: {elapsed_time}")
        except Exception as e:
            print("The robot could not reach the requested position.")
            print("Error:", e)
        counter += 1


if __name__ == '__main__':
    
    robot = pyniryo.NiryoRobot(IP) #192.168.10.178
    try:
        main(robot)
    except KeyboardInterrupt:
        robot.arm.go_to_sleep()            
        # robot.pick_place.pick_from_pose(pos)
        print("The robot got stopped.")
        robot.end()

