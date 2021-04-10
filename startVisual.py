from kubipy.utils import minipy
import webbrowser

from scripts import sCall, sOpen, sKill
from kubipy.utils import minipy

def openPorts():
    grafanaInstance = sOpen('kubectl port-forward svc/visualizer-release-grafana 3000:80')
    influxInstance = sOpen('kubectl port-forward svc/visualizer-release-influxdb 8086:8086')

if __name__ == '__main__':
    sCall("minikube start")
    openPorts()
    #webbrowser.open("Site/index.html")
    webbrowser.open("http://localhost:3000/d/tPOgznlMz/sensor-dashboard?orgId=1")