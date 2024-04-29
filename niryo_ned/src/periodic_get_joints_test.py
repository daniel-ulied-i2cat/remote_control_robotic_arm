from prometheus_client import start_http_server, Gauge
import random
import time
import pyniryo2 as pyniryo


def main(robot: pyniryo.NiryoRobot, example_metric: Gauge) -> None:

    robot.arm.calibrate_auto()
    
    print("Creating http server")
    # Start the Prometheus HTTP server on the specific IP address and port
    start_http_server(8000)
    print("Starting to read arm.get_joints!")
    example_metric.set(0)

    while True:
        start_time = time.time()
        robot.arm.get_joints()
        example_metric.set(time.time() - start_time)

if __name__ == '__main__':
    example_metric = Gauge('Movement_Time', 'Time it takes to move from a given position to another given position')
    robot = pyniryo.NiryoRobot("172.27.13.150")
    try:
        main(robot, example_metric)
    except KeyboardInterrupt:
        robot.end()
