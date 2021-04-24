import webbrowser
import os

from scripts import sCall, sOpen, sKill, sReturn

def openPorts():
    grafanaInstance = sOpen('kubectl port-forward svc/visualizer-release-grafana 3000:80')
    influxInstance = sOpen('kubectl port-forward svc/visualizer-release-influxdb 8086:8086')


if __name__ == '__main__':
    podStatus = sReturn("kubectl get pods")
    if "0/1" in podStatus:
        print("InfluxDB is still setting up. Please try again in ~30s")
        exit()
    if ''.join(filter(str.isalpha, sReturn("echo $INFLUX_TOKEN")))=="":
        print("Setting up InfluxDB Auth")
        token=sReturn('kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-token}" | base64 --decode')
        os.environ["INFLUX_TOKEN"]=token #temporary - os can't permanently change variables
        print("InfluxDB Admin Token: "+token)
        password=sReturn('kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-password}" | base64 --decode')
        os.environ["INFLUX_PASSWORD"]=password
        print("InfluxDB Admin Password: "+password)
        sCall('influx config create -n default -t '+token+' -a -u http://localhost:8086')
        sCall('export INFLUX_ACTIVE_CONFIG="default"')
        sCall('influx config default')
        sCall('influx org create -n vis-org')
        sCall('export INFLUX_ORG="vis-org"')
        sCall('influx auth create --read-buckets --read-checks --read-dashboards --read-dbrps --read-notificationEndpoints --read-notificationRules --read-orgs --read-tasks --read-telegrafs --read-user --write-buckets --write-checks --write-dashboards --write-dbrps --write-notificationEndpoints --write-notificationRules --write-orgs --write-tasks --write-telegrafs --write-user')
        exit()
    openPorts()
    webbrowser.open("http://localhost:3000/d/tPOgznlMz/sensor-dashboard?orgId=1")
