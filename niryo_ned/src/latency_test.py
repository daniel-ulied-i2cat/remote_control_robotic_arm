from prometheus_client import start_http_server, Gauge
import random
import time
import pyniryo2 as pyniryo


def main(robot: pyniryo.NiryoRobot, example_metric: Gauge) -> None:

    robot.arm.calibrate_auto()
    
    print("Creating http server")
    # Start the Prometheus HTTP server on the specific IP address and port
    start_http_server(8000)

    while True:
        start_time = time.time()
        robot.arm.move_joints([0.0, -0.059, 1.170, 0.0, 0.0, 0.0])
        example_metric.set(time.time() - start_time)
        
        middle_time = time.time()
        robot.arm.move_joints([0.0, 0.5, -1.251, 0.0, 0.0, 0.0])
        example_metric.set(time.time() - middle_time)

if __name__ == '__main__':
    example_metric = Gauge('Movement_Time', 'Time it takes to move from a given position to another given position')
    robot = pyniryo.NiryoRobot("192.168.10.178")
    try:
        main(robot, example_metric)
    except KeyboardInterrupt:
        robot.end()
