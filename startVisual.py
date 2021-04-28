import webbrowser
import os
import json
import base64

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
        print("InfluxDB Admin Username: admin")
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
        
        runInPod("grafana","grafana-cli plugins install grafana-worldmap-panel")
        
        sCall('curl -X POST -H "Content-Type: application/json" -d \'{"name":"apiorg"}\' http://admin:password@localhost:3000/api/orgs')
        sCall('curl -X POST http://admin:password@localhost:3000/api/user/using/2')
        data=json.loads(sReturn('curl -X POST -H "Content-Type: application/json" -d \'{"name":"apikeycurl", "role": "Admin"}\' http://admin:password@localhost:3000/api/auth/keys'))
        if "key" in data:
            grafanaToken=json.loads(base64.b64decode(data["key"]).decode("UTF-8"))["k"]
            print("Grafana Admin Token: "+grafanaToken)

        with open('./payload.json') as f:
            payload=json.dumps(json.load(f))
        print(sReturn('curl -X POST --insecure -H "Authorization: Bearer '+data["key"]+'" -H "Content-Type: application/json" -d '+ payload +' http://admin:password@localhost:3000/api/dashboards/db'))
        
    print("\nGrafana Username: 'admin'\nGrafana Password: 'password'")
    webbrowser.open("http://localhost:3000/")
