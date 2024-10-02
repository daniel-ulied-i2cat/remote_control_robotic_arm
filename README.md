# Remote Control Niryo Ned 2

Repository for the Remote Control of Niryo Ned 2. 

## Niryo Ned 2

The Niryo Ned 2 is a robotic arm that runs on open-source software (https://github.com/NiryoRobotics/ned_ros). The code is designed based on ROS, where there are a number of different ROS nodes, each running a specific component of the robots hardware (there are also other support ROS nodes).

## How to use it?

To deploy this code there are two possible ways;

1. Use the Dockerfile;

1.1 Generate the Dockerfile;

```docker build . -t remote_controller```

1.2 Launch the Docker Container;

```docker run -t remote_controller```

2. Launch Locally;

2.1 Create Python Virtual Environment

```python -m venv .venv```

2.2 Source Virtual Environment

```source .venv/bin/activate```

2.3 Install Dependancies

```pip install -r requirements.txt```

2.4 Launch Python Project

```python main.py```

## Expected Results;

A prometheus graph should be present in URL: http://localhost:9001. With information regarding the time it has taken to move the armL

