# Remotr Control Niryo Ned 2

Repository for the Remote Control of Niryo Ned 2. 

Also, the porject includes monitoring. The monitoring is going to be done using Prometheus and then visualized in Grafana. Monitoring should include latency, jitter and throughput.


## Project Status

### 29/04/2024

First commit to the repository. Currently the project contains Python scripts to run tests, as well as docker and docker-compose files to run the tests in a containarized manner.

## Roadmap

- [x] Run Remote Control in Docker
- [x] Add Prometheus
- [ ] Add Grafana
- [ ] Add Latency, Jitter, Throughput to Prometheus
- [ ] Create a remote control interface. Maybe keyboard to move arm (or directly in Grafana?)
