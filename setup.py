from kubipy.utils import minipy
from avionix import ChartBuilder, ChartInfo, ChartDependency

from scripts import sCall, sReturn


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
                    "influxdata",
                    "1.8.4",
                    "https://helm.influxdata.com/",
                    "influxdata/influxdb"
                )
        ],
    ),
    [],
)
builder.install_chart()

sCall("export INFLUX_TOKEN='OLd40qlqzgOHyhUnQT29'")

sCall("chmod -R +x ./")

print("Installation complete!\nRun 'python3 startVisual.py' to start the program")