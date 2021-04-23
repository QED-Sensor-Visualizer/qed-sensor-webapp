import os
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Error: Requires Python 3.x\n")
    sys.exit(1)
import shutil

from kubernetes import client, config
from avionix import ChartBuilder, ChartInfo, ChartDependency

from scripts import sCall, sReturn, getMinikube
import startVisual
import stopVisual

def kubStatus():
    try: config.load_kube_config()
    except: 
        print("Error: Requires an active Kubernetes Cluster or Minikube Instance")
        print("Install Minikube? This requires a Homebrew install.")
        answer=input().upper()
        if "Y" in answer:
            getMinikube()
        else:
            sys.exit()

if len(sys.argv)==0 or not "--skipMinikube" in sys.argv:
    kubStatus()

print("Checking Helm...")
sCall("curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3")
sCall("chmod 700 get_helm.sh")
sCall("./get_helm.sh")
sCall("rm get_helm.sh")


helmV=str(sReturn("helm version"))
helmV=helmV[helmV.index("Version:")+10:helmV.index("\",")]

if os.path.isdir("./visualizer-release"):
    print("Removing previous installation")
    shutil.rmtree("./visualizer-release")
else: print("No previous installation was found")

print("Generating Helm Charts...")
builder = ChartBuilder(
    ChartInfo(
        api_version=helmV,
        name="visualizer-release",
        version="0.1.0",
        app_version="v1",
        dependencies=[
                ChartDependency(
                    "grafana",
                    "6.7.3",
                    "https://grafana.github.io/helm-charts",
                    "helm-charts"
                    #values={"admin":{"userKey":"admin","passwordKey":"password"}}
                ),
                ChartDependency(
                    "influxdb",
                    "2.2.1",
                    "https://charts.bitnami.com/bitnami",
                    "bitnami/influxdb"
                ),
                ChartDependency(
                    "telegraf",
                    "1.7.38",
                    "https://influxdata.github.io/helm-charts",
                    "influxdata/telegraf"
                )
        ],
    ),
    [],
)

sCall("helm repo remove grafana")
sCall("helm repo remove influxdata/influxdb")
sCall("helm repo remove influxdata/telegraf")
builder.install_chart({"dependency-update": None})
sCall("chmod -R +x ./")
sCall('kubectl exec --namespace default -it -- $(kubectl get pods --namespace default -l "app=grafana,release=grafana" -o jsonpath="{.items[0].metadata.name}") grafana-cli admin reset-admin-password password')
startVisual.openPorts()

sCall('export INFLUX_TOKEN=$(kubectl get secret --namespace "default" influxdb -o jsonpath="{.data.admin-user-token}" | base64 --decode)')
sCall('influx config create -n default -t $INFLUX_TOKEN -a -u http://localhost:8086')
sCall('export INFLUX_ACTIVE_CONFIG="default"')
sCall('influx config default')
sCall('influx org create -n vis-org')
sCall('export INFLUX_ORG="vis-org"')
sCall('influx auth create --read-buckets --read-checks --read-dashboards --read-dbrps --read-notificationEndpoints --read-notificationRules --read-orgs --read-tasks --read-telegrafs --read-user --write-buckets --write-checks --write-dashboards --write-dbrps --write-notificationEndpoints --write-notificationRules --write-orgs --write-tasks --write-telegrafs --write-user')

stopVisual.closePorts()
print("Installation complete!\nRun 'python3 startVisual.py' to start the program")
