from scripts import sCall, sReturn

sCall("kubectl delete svc visualizer-release-grafana visualizer-release-influxdb visualizer-release-telegraf")
sCall("kubectl delete statefulsets visualizer-release-influxdb")
sCall("kubectl delete deployments visualizer-release-grafana visualizer-release-influxdb visualizer-release-telegraf")