import webbrowser
import os
import json
import base64
import pexpect
import requests as req

from scripts import sCall, sOpen, sKill, sReturn, runInPod


def openPorts():
    grafanaInstance = sOpen(
        'kubectl port-forward svc/visualizer-release-grafana 3000:80')
    influxInstance = sOpen(
        'kubectl port-forward svc/visualizer-release-influxdb 8086:8086')


if __name__ == '__main__':
    podStatus = sReturn("kubectl get pods")
    if "0/1" in podStatus:
        print("InfluxDB is still setting up. This can take up to 2 minutes.")
        exit()

    openPorts()
    if ''.join(filter(str.isalpha, sReturn("echo $INFLUX_TOKEN"))) == "":
        print("Setting up InfluxDB Auth")
        token = sReturn(
            'kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-token}" | base64 --decode')
        # temporary - os can't permanently change variables
        os.environ["INFLUX_TOKEN"] = token
        print("InfluxDB Admin Token: "+token)
        print("InfluxDB Admin Username: admin")

        child = pexpect.spawn("influx user password -t "+token+" -n 'admin'")
        try:
            child.expect("password", timeout=3)
            child.sendline("password")
            child.expect("password", timeout=3)
            child.sendline("password")
        except:
            print(
                "Error reaching Influx. Please wait 5 seconds and rerun 'python3 startVisual.py'")
            exit()
            raise
        # password = sReturn(
        #    'kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-password}" | base64 --decode')
        # os.environ["INFLUX_PASSWORD"] = password
        print("InfluxDB Admin Password: password")

        sCall('influx config create -n default -t ' +
              token+' -a -u http://localhost:8086')
        sCall('influx config default')
        sCall('influx org create -n vis-org')
        sCall('influx auth create --read-buckets --read-checks --read-dashboards --read-dbrps --read-notificationEndpoints --read-notificationRules --read-orgs --read-tasks --read-telegrafs --read-user --write-buckets --write-checks --write-dashboards --write-dbrps --write-notificationEndpoints --write-notificationRules --write-orgs --write-tasks --write-telegrafs --write-user')

        sCall('influx bucket create -n "vis-bucket" -o "vis-org" -t '+token)
        influxIP = sReturn('kubectl get svc --namespace default | grep influx')
        influxIP = "http://" + \
            influxIP[influxIP.find("IP")+2:influxIP.find("<")]+":8086"
        print("InfluxDB URL: "+influxIP)

        runInPod("grafana", "grafana-cli plugins install grafana-worldmap-panel")

        sCall(
            'curl -X POST -H "Content-Type: application/json" -d \'{"name":"apiorg"}\' http://admin:password@localhost:3000/api/orgs')
        sCall('curl -X POST http://admin:password@localhost:3000/api/user/using/2')
        data = json.loads(sReturn(
            'curl -X POST -H "Content-Type: application/json" -d \'{"name":"apikeycurl", "role": "Admin"}\' http://admin:password@localhost:3000/api/auth/keys'))

        if "key" in data:
            grafanaToken = json.loads(base64.b64decode(
                data["key"]).decode("UTF-8"))["k"]
            print("Grafana Admin Token: "+grafanaToken)
            with open('./source.json') as f:
                rawJson = json.load(f)
                rawJson["url"] = influxIP
                payload = json.dumps(rawJson)
            print(sReturn('curl -X POST --insecure -H "Content-Type: application/json" -d \'' +
                  payload + '\' http://admin:password@localhost:3000/api/dashboards/db'))
            headers = {"Accept": "application/json","Content-Type": "application/json"}
            dashboard = {"id": None,
                "title": "Sensor Data",
                "tags": ["vis-autoGen"],
                "timezone": "browser",
                "rows": [{}],
                "schemaVersion": 6,
                "version": 0
            }
            payload = {"dashboard": dashboard}
            url = "http://admin:password@localhost:3000/api/dashboards/db"
            p = req.post(url, headers=headers, json=payload)

    print("\nGrafana Username: 'admin'\nGrafana Password: 'password'")
    # webbrowser.open("http://localhost:3000/")
