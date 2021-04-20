# QED Sensor Visualizer

A visualizer for multi-modal sensor data, built using the TIG Stack (Telegraf, InfluxDB, and Grafana) and deployable through Kubernetes. Supports time series data of different frequencies and video footage, viewable together through one interface.

## Installation

This visualizer requires an active Kubernetes cluster or Minikube instance.

Python3 is also required, along with several Pip packages. To install, run the following commands:

```bash
pip install kubernetes
pip install avionix
```

The following Pip package is not required but can be used to install Minikube if Kubernetes/Docker is not set up:

```bash
pip install kubipy
```

To set up the visualizer, run the setup script:

```bash
python3 setup.py

#Optional arguments: '--skipMinikube' (skip the fallback Minikube installation) 
```

This script verifies your Helm installation and generates an umbrella chart containing all the programs, which is deployed onto your current Kubernetes cluster. It also automatically sets up authentication info for the various components:

```bash
Grafana:
   admin.adminKey: admin
   admin.passwordKey: password

InfluxDB:
   Default Organization: vis-org
```

## Usage

To start and stop the visualizer, you can run the following commands, respectively:

```bash
python3 startVisual.py
python3 stopVisual.py
```

Once started, the visualizer will be usable in a webapp hosted at [localhost:3000](http://localhost:3000/).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
