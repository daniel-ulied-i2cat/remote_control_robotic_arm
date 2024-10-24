import random
import time
import pyniryo2 as pyniryo
import numpy as np
import threading

IP = "localhost"

def open_close_gripper(robot, gripped: bool) -> bool:
    if not gripped:
        robot.tool.open_gripper()
        gripped = True
    else:
        robot.tool.close_gripper()
        gripped = False
    return gripped


def main(robot, gripped):
    movement_counter = 0
    grasp_times = []
    grasp_time = time.time()
    while True:
        if round(robot.arm.joints[1], 2) ==  -0.5 and round(robot.arm.joints[2], 2) == -0.85:
            gripped = open_close_gripper(robot, gripped)
            movement_counter += 1
            grasp_times.append(time.time() - grasp_time)
            print("Grasp Current Period: " + str(time.time() - grasp_time))
            average = sum(grasp_times) / len(grasp_times)
            print("Average Grasp Period: " + str(average))
            variance = sum((x - average) ** 2 for x in grasp_times) / (len(grasp_times) - 1) if len(grasp_times) > 1 else 0
            print("Variance Grasp Period: " + str(variance))
            print("Tracked Movements: " +  str(movement_counter))
            print("\033[F\033[F\033[F\033[F\033[F")
            grasp_time = time.time()
            time.sleep(1)

if __name__ == '__main__':

    robot = pyniryo.NiryoRobot(IP)
    
    try:
        main(robot, False)
    except KeyboardInterrupt:
        print("\n\n\n\n")
        print("Exiting...")

