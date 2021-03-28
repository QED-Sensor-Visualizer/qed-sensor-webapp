import subprocess

from kubipy.utils import minipy
from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller

def sCall(cmd):
    subprocess.call(cmd,shell=True)

#minikube installation
cluster=minipy(False)
cluster.install()


#helm charts
tiller = Tiller(TILLER_HOST)
chart = ChartBuilder({"name": "nginx-ingress", "source": {"type": "repo", "location": "https://kubernetes-charts.storage.googleapis.com"}})
tiller.install_release(chart.get_helm_chart(), dry_run=False, namespace='default')