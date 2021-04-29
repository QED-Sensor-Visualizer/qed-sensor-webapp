import os
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Error: Requires Python 3.x\n")
    sys.exit(1)
import shutil

from kubernetes import client, config
from avionix import ChartBuilder, ChartInfo, ChartDependency

from scripts import sCall, sReturn, getMinikube, runInPod
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
if sReturn("helm").index("ubernetes")==-1:
    sCall("curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3")
    sCall("chmod 700 get_helm.sh")
    sCall("./get_helm.sh")
    sCall("rm get_helm.sh")
helmV=str(sReturn("helm version"))
helmV=helmV[helmV.index("Version:")+10:helmV.index("\",")]

print("Generating Helm Charts...")
sCall("helm repo add grafana https://grafana.github.io/helm-charts")
sCall("helm repo add bitnami https://charts.bitnami.com/bitnami")
sCall("helm repo add influxdata https://influxdata.github.io/helm-charts")
sCall("helm repo update")

sCall("helm install visualizer-release-grafana grafana/grafana")
sCall("helm install visualizer-release-influxdb bitnami/influxdb")
sCall("helm install visualizer-release-telegraf influxdata/telegraf")

sCall("chmod -R +x ./")
runInPod("grafana","grafana-cli admin reset-admin-password password")

print("Installation complete!\nRun 'python3 startVisual.py' to start the program")
