from scripts import sCall, sReturn
from kubipy.utils import minipy

from stopVisual import closePorts

closePorts()
sCall("kubectl delete statefulsets visualizer-release-influxdb")
sCall("kubectl delete deployments visualizer-release-grafana visualizer-release-influxdb visualizer-release-telegraf")
sCall("helm uninstall visualizer-release-grafana visualizer-release-influxdb visualizer-release-telegraf")