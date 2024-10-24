import random
import time
import pyniryo2 as pyniryo
import numpy as np
import threading

IP = "localhost"

def main(robot, gripped):
    before = time.time()
    if not gripped:
        print("Closing gripper")
        robot.tool.close_gripper()
        gripped = True
    else:
        print("Opening gripper")
        robot.tool.open_gripper()
        gripped = False

    print("Gripped in: " + str(time.time() - before))
    threading.Timer(5.43, main, args=(robot,gripped)).start()

if __name__ == '__main__':

    robot = pyniryo.NiryoRobot(IP) #192.168.10.178
    
    try:
        main(robot, False)
        while True:
            pass
    except KeyboardInterrupt:
        print("Going to sleep, please wait...")

