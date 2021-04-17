import webbrowser

from scripts import sCall, sOpen, sKill

def openPorts():
    grafanaInstance = sOpen('kubectl port-forward svc/visualizer-release-grafana 3000:80')
    influxInstance = sOpen('kubectl port-forward svc/visualizer-release-influxdb 8086:8086')

if __name__ == '__main__':
    openPorts()
    webbrowser.open("http://localhost:3000/d/tPOgznlMz/sensor-dashboard?orgId=1")