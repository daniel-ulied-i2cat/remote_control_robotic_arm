from prometheus_client import start_http_server, Gauge
import random
import time
import pyniryo

# Create a Prometheus metric (Gauge in this example)
example_metric = Gauge('Movement_Time', 'Time it takes to move from a given position to another given position')

def main():
      
    robot = pyniryo.NiryoRobot("localhost")

    robot.calibrate_auto()
    
    print("Creating http server")
    # Start the Prometheus HTTP server on the specific IP address and port
    start_http_server(port=8000, addr='172.25.144.1')

    pick_pose = pyniryo.PoseObject(
    x=0.30, y=0.0, z=0.15,
    roll=0, pitch=1.57, yaw=0.0
    )
    first_place_pose = pyniryo.PoseObject(
        x=0.0, y=0.2, z=0.15,
        roll=0, pitch=1.57, yaw=0.0
    )
    while True:
        start_time = time.time()
        robot.move_pose(pick_pose)
        example_metric.set(time.time() - start_time)
        
        middle_time = time.time()
        robot.move_pose(first_place_pose)
        example_metric.set(time.time() - middle_time)

if __name__ == '__main__':
    main()
