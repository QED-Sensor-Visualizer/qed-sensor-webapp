from kubipy.utils import minipy
import webbrowser

from scripts import sCall, sOpen, sKill

def openPorts():
    grafanaInstance = sOpen('kubectl --namespace default port-forward $(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=visualizer-grafana-release" -o jsonpath="{.items[0].metadata.name}") 3000')
    influxInstance = sOpen('kubectl --namespace default port-forward influxdb-release-5ccfb5b4d9-mwzd2 8086')

if __name__ == '__main__':
    openPorts()
    #webbrowser.open("Site/index.html")
    webbrowser.open("http://localhost:3000/d/tPOgznlMz/sensor-dashboard?orgId=1")