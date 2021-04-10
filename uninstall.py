from scripts import sCall, sReturn
from kubipy.utils import minipy

sCall("kubectl delete svc visualizer-release-grafana visualizer-release-influxdb visualizer-release-telegraf")
sCall("kubectl delete statefulsets visualizer-release-influxdb")
sCall("kubectl delete deployments visualizer-release-grafana visualizer-release-influxdb visualizer-release-telegraf")

#cluster=minipy(False)
#cluster.stop()
#cluster.delete()