from prometheus_client import start_http_server, Gauge

PROMETHEUS_CLIENT_PORT = 8000


class PrometheusClient:

    def __init__(self) -> None:
        self.prometheus_client_port = PROMETHEUS_CLIENT_PORT
        self.latency_gauge = Gauge('latency', 'Network Latency Round Trip Time')
        self.joint_movement_time = Gauge('joint_movement_time', 'Time taken to move joint from current to target position')
        self.throughput = Gauge('throughput', 'Mbps used to send Niryo-related data')

        start_http_server(self.prometheus_client_port)

    def send_latency(self, value: str) -> None:
        self.latency_gauge.set(value)

    def send_joint_movement_time(self, value: str) -> None:
        self.joint_movement_time.set(value)

    def send_throughput(self, value: str) -> None:
        self.throughput.set(value)