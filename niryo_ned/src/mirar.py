#from prometheus_client import start_http_server, Gauge
import time
import pyniryo2 as pyniryo

IP = "172.27.13.150"

def main(robot: pyniryo.NiryoRobot) -> None:
    robot.arm.calibrate_auto()
    
    print("Creating HTTP server")
    # Start the Prometheus HTTP server on port 8000
    #start_http_server(8000)
    #print("Starting to read arm.get_joints!")
    #example_metric.set(0)

    last_joint_positions = None

    while True:
        start_time = time.time()
        current_joint_positions = robot.arm.get_joints()
        if current_joint_positions != last_joint_positions:
            print("Joint positions updated:", current_joint_positions)
            #example_metric.set(time.time() - start_time)
            #print(f"Current Time Value: {example_metric._value.get()} seconds")
            last_joint_positions = current_joint_positions
        else:
            print("No change in joint positions.")
        
        # Optional: sleep to prevent the loop from running too fast
        time.sleep(1)

if __name__ == '__main__':
    #example_metric = Gauge('Movement_Time', 'Time it takes to move from a given position to another given position')
    robot = pyniryo.NiryoRobot(IP)
    try:
        main(robot)
    except KeyboardInterrupt:
        print("Interrupt received, stopping the robot.")
        robot.end()
    except Exception as e:
        print(f"An error occurred: {e}")
        robot.end()


