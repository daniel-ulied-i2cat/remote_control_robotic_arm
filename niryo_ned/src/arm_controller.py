import time
import pyniryo2 as pyniryo
import termios
import tty
import sys
import select

IP = "172.27.13.150"
INITIAL_POSITION = [0, 0.499, -1.248, 0, 0, 0]
STEP_SIZE = 0.05

def disable_echo():
    fd = sys.stdin.fileno()
    original_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    new_settings = termios.tcgetattr(fd)
    new_settings[3] &= ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
    return original_settings

def restore_terminal(original_settings):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)

def get_key() -> str:
    original_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)
    return key

def animate():
    animation = ["Moving...   ", "Moving..    ", "Moving...   "]
    for frame in animation:
        sys.stdout.write(f"\r{frame}")
        sys.stdout.flush()
        time.sleep(0.2)

def main(robot: pyniryo.NiryoRobot) -> None:
    """
         joint0: Base Motor -> -2.99 <-> 2.99 
           - Controls the rotation of the robot's base
           - Positive Values (>0): Rotate right
           - Negative Values (<0): Rotate left
        
         joint1: Shoulder Motor -> -1.83 <-> 0.61
           - Moves the shoulder of the robot arm
           - Positive Values (>0): Raise the shoulder upward
           - Negative Values (<0): Lower the shoulder downward
        
         joint2: Elbow Motor -> -1.34 <-> 1.57
           - Moves the elbow of the robot arm
           - Positive Values (>0): Raise the elbow upward
           - Negative Values (<0): Lower the elbow downward
        
         joint3: Forearm Rotation Motor -> -2.09 <-> 2.09
           - Rotates the wrist of the robot arm
           - Positive Values (>0): Rotate wrist to the right
           - Negative Values (<0): Rotate wrist to the left
        
         joint4: Wrist Motor -> -1.92 <-> 1.92
           - Moves the fingers of the robot up and down
           - Positive Values (>0): Move fingers upward
           - Negative Values (<0): Move fingers downward
        
         joint5: Hand Rotation Motor -> -2.53 <-> 2.53
           - Rotates or actuates the end effector or gripper
           - Positive Values (>0): Rotate the gripper to the right
           - Negative Values (<0): Rotate the gripper to the left
    """
    robot.arm.calibrate_auto()
    settings = termios.tcgetattr(sys.stdin)
    pos = INITIAL_POSITION
    current_key = None
    key_count = 0

    actions = {
        'i': ("Shoulder", 1),
        'k': ("Shoulder", 1),
        'l': ("Base", 0),
        'j': ("Base", 0),
        'w': ("Elbow", 2),
        's': ("Elbow", 2),
        'a': ("Forearm", 3),
        'd': ("Forearm", 3),
        ' ': ("Grip", 4),
    }

    try:
        while True:
            key = get_key()
            if key in actions:
                joint_name, joint_index = actions[key]

                if key == current_key:
                    key_count += 1
                else:
                    current_key = key
                    key_count = 1

                # Wait until the key is released
                while key == current_key:
                    key = get_key()

                # Calculate the step based on the key count
                step = STEP_SIZE * key_count

                # Update position based on the action
                if key in ['i', 'k']:
                    pos[joint_index] += step if key == 'i' else -step
                elif key in ['l', 'j']:
                    pos[joint_index] += step if key == 'l' else -step
                elif key in ['w', 's']:
                    pos[joint_index] += step if key == 'w' else -step
                elif key in ['a', 'd']:
                    pos[joint_index] += -step if key == 'a' else step
                elif key == ' ':
                    pos[joint_index] += step

                # Enforce joint limits
                pos[0] = max(-2.99, min(2.99, pos[0]))
                pos[1] = max(-1.83, min(0.61, pos[1]))
                pos[2] = max(-1.34, min(1.57, pos[2]))
                pos[3] = max(-2.09, min(2.09, pos[3]))
                pos[4] = max(-1.92, min(1.92, pos[4]))
                pos[5] = max(-2.53, min(2.53, pos[5]))

                # Print moving animation
                sys.stdout.write(f"\rMoving...                                                ")
                sys.stdout.flush()
                animate()

                # Move the robot
                time_before_command = time.time()
                robot.arm.move_joints(pos)
                time_taken = time.time() - time_before_command

                # Print the moved message
                sys.stdout.write(f"\rMoved {joint_name} by {step:.2f} in {time_taken:.2f} seconds.\n")
                sys.stdout.flush()
                sys.stdout.write(f"\033[F")  # Move cursor up one line

            elif key == 'q':
                break  # Exit loop if 'q' is pressed

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    original_settings = disable_echo()
    robot = pyniryo.NiryoRobot(IP)
    try:
        main(robot)
    except KeyboardInterrupt:
        robot.arm.go_to_sleep()
        print("The robot got stopped.")
    finally:
        robot.end()
        restore_terminal(original_settings)
