import webbrowser
import os
import json
from grafana_api.grafana_face import GrafanaFace

from scripts import sCall, sOpen, sKill, sReturn, runInPod

def openPorts():
    grafanaInstance = sOpen('kubectl port-forward svc/visualizer-release-grafana 3000:80')
    influxInstance = sOpen('kubectl port-forward svc/visualizer-release-influxdb 8086:8086')


if __name__ == '__main__':
    podStatus = sReturn("kubectl get pods")
    if "0/1" in podStatus:
        print("InfluxDB is still setting up. Please try again in ~30s")
        exit()

    openPorts()
    if ''.join(filter(str.isalpha, sReturn("echo $INFLUX_TOKEN")))=="":
        print("Setting up InfluxDB Auth")
        token=sReturn('kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-token}" | base64 --decode')
        os.environ["INFLUX_TOKEN"]=token #temporary - os can't permanently change variables
        print("InfluxDB Admin Token: "+token)
        password=sReturn('kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-password}" | base64 --decode')
        os.environ["INFLUX_PASSWORD"]=password
        print("InfluxDB Admin Password: "+password)
        #unInPod('influx','influx config create -n default -t '+token+' -a -u http://localhost:8086')
        #runInPod('influx','influx config default')
        #runInPod('influx','influx org create -n vis-org')
        #runInPod('influx','influx auth create --read-buckets --read-checks --read-dashboards --read-dbrps --read-notificationEndpoints --read-notificationRules --read-orgs --read-tasks --read-telegrafs --read-user --write-buckets --write-checks --write-dashboards --write-dbrps --write-notificationEndpoints --write-notificationRules --write-orgs --write-tasks --write-telegrafs --write-user')
        sCall('influx config create -n default -t '+token+' -a -u http://localhost:8086')
        sCall('influx config default')
        sCall('influx org create -n vis-org')
        sCall('influx auth create --read-buckets --read-checks --read-dashboards --read-dbrps --read-notificationEndpoints --read-notificationRules --read-orgs --read-tasks --read-telegrafs --read-user --write-buckets --write-checks --write-dashboards --write-dbrps --write-notificationEndpoints --write-notificationRules --write-orgs --write-tasks --write-telegrafs --write-user')
        
        sCall('influx bucket create -n "vis-bucket" -o "vis-org" -t '+token)
        influxIP=sReturn('kubectl get svc --namespace default | grep influx |awk "{print $3}"')
        influxURL="http://"+influxIP+":8086"

        print(influxURL)
        grafana_api = GrafanaFace(
            auth=("admin","password"),
            host="http://localhost:3000"
        )
        with open("./test.json") as f:
            data=json.load(f)
        grafana_api.dashboard.update_dashboard(dashboard={'dashboard': data, 'folderId': 0, 'overwrite': True})
        
    #webbrowser.open("http://localhost:3000/")
