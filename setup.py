from kubipy.utils import minipy
from avionix import ChartBuilder, ChartInfo, ChartDependency

from scripts import sCall, sReturn
import startVisual
import stopVisual

"""
print("Installing Minikube...")
#minikube installation
cluster=minipy(False)
cluster.install()


#HELM
print("Installing Helm...")
sCall("curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3")
sCall("chmod 700 get_helm.sh")
sCall("./get_helm.sh")
sCall("rm get_helm.sh")
"""

helmV=str(sReturn("helm version"))
helmV=helmV[helmV.index("Version:")+10:helmV.index("\",")]

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
                    "6.6.4",
                    "https://grafana.github.io/helm-charts",
                    "helm-charts",
                    values={"admin":{"userKey":"admin","passwordKey":"password"}}
                ),
                ChartDependency(
                    "influxdb",
                    "1.8.4",
                    "https://influxdata.github.io/helm-charts",
                    "influxdata/influxdb"
                ),
                ChartDependency(
                    "telegraf",
                    "1.18.0",
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
startVisual.openPorts()

sCall('export INFLUX_TOKEN=$(kubectl get secret --namespace "default" influxdata -o jsonpath="{.data.admin-user-token}" | base64 --decode)')
sCall('influx config create -n default -t $INFLUX_TOKEN -a -u http://localhost:8086')
sCall('export INFLUX_ACTIVE_CONFIG="default"')
sCall('influx config default')
sCall('influx org create -n vis-org')
sCall('export INFLUX_ORG="vis-org"')
sCall('influx auth create --read-buckets --read-checks --read-dashboards --read-dbrps --read-notificationEndpoints --read-notificationRules --read-orgs --read-tasks --read-telegrafs --read-user --write-buckets --write-checks --write-dashboards --write-dbrps --write-notificationEndpoints --write-notificationRules --write-orgs --write-tasks --write-telegrafs --write-user')

stopVisual.closePorts()
print("Installation complete!\nRun 'python3 startVisual.py' to start the program")