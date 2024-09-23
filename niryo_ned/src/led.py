import random
import time
import pyniryo2 as pyniryo

import numpy as np

IP = "172.27.13.150"

robot = pyniryo.NiryoRobot(IP)
robot.led_ring.solid([15, 50, 255])
robot.led_ring.solid([255, 255, 255])